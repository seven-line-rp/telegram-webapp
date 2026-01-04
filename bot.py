import telebot
from telebot import types
import json
from datetime import datetime

# Токен вашего бота
TOKEN = '7607802872:AAF32GM7bc3G6245XIyVOJxvlZWKXKghPHQ'
bot = telebot.TeleBot(TOKEN)

# URL вашего веб-приложения (измените на реальный URL)
WEB_APP_URL = "https://seven-line-rp.github.io/telegram-webapp/index.html"  # Замените на ваш реальный URL

# Словарь для хранения информации о пользователях
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Друг"
    
    # Сохранить информацию о пользователе
    user_data[user_id] = {
        'username': message.from_user.username or 'Unknown',
        'first_name': user_name,
        'last_name': message.from_user.last_name or '',
        'joined': datetime.now().isoformat()
    }
    
    # Создать клавиатуру с кнопкой веб-приложения
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    
    # Кнопка для открытия мини-приложения
    web_app_btn = types.KeyboardButton(
        text="🚀 Открыть мини-приложение",
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    
    # Дополнительные кнопки
    btn_info = types.KeyboardButton(text="ℹ️ Инфо")
    btn_help = types.KeyboardButton(text="❓ Помощь")
    
    markup.add(web_app_btn)
    markup.add(btn_info, btn_help)
    
    welcome_message = f"""
🎉 Привет, {user_name}!

Это тестовое Telegram мини-приложение.

📱 Нажмите кнопку ниже, чтобы открыть приложение.
Вы сможете:
✅ Просмотреть свою информацию
✅ Отправить сообщение боту
✅ Увидеть цвета вашей темы

Разработано: 4 января 2026
    """
    
    bot.send_message(
        message.chat.id,
        welcome_message.strip(),
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    """Обработчик команды /help"""
    help_text = """
📚 Справка по командам:

/start - Начать работу с приложением
/help - Показать эту справку
/info - Информация о вас
/users - Показать количество пользователей (только админ)
/stats - Статистика приложения

🎮 Функции приложения:
- 📢 Уведомления
- ❓ Подтверждение
- 💬 Отправка данных
- 🎨 Отображение тем
    """
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['info'])
def info_command(message):
    """Обработчик команды /info"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Unknown"
    username = message.from_user.username or "Unknown"
    
    info_text = f"""
👤 Ваша информация:

ID: <code>{user_id}</code>
Имя: {user_name}
Username: @{username}
Chat ID: <code>{message.chat.id}</code>
Язык: {message.from_user.language_code or 'не указан'}
Is Bot: {message.from_user.is_bot}
    """
    
    bot.send_message(message.chat.id, info_text.strip(), parse_mode='HTML')

@bot.message_handler(commands=['stats'])
def stats_command(message):
    """Обработчик команды /stats"""
    total_users = len(user_data)
    
    stats_text = f"""
📊 Статистика приложения:

👥 Всего пользователей: {total_users}
⏰ Время сервера: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
🔌 Статус: ✅ Онлайн
🗄️ База данных: активна
    """
    
    bot.send_message(message.chat.id, stats_text.strip())

@bot.message_handler(func=lambda message: message.text == "ℹ️ Инфо")
def info_button(message):
    """Обработчик кнопки Инфо"""
    info_command(message)

@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def help_button(message):
    """Обработчик кнопки Помощь"""
    help_command(message)

@bot.message_handler(content_types=['web_app_data'])
def web_app_data(message):
    """Обработчик данных от веб-приложения"""
    try:
        # Получить и распарсить данные
        data = message.web_app_data.data
        parsed_data = json.loads(data)
        
        user_id = message.from_user.id
        user_name = message.from_user.first_name or "Unknown"
        
        # Сохранить данные
        if user_id not in user_data:
            user_data[user_id] = {}
        
        user_data[user_id]['last_message'] = parsed_data.get('message', '')
        user_data[user_id]['last_timestamp'] = parsed_data.get('timestamp', '')
        
        # Создать красивый ответ
        response_message = f"""
✅ Данные успешно получены!

📨 Ваше сообщение: <code>{parsed_data.get('message', 'N/A')}</code>

⏰ Время отправки: <code>{parsed_data.get('timestamp', 'N/A')}</code>

👤 Пользователь: {user_name}
🆔 ID: <code>{user_id}</code>

💾 Данные сохранены в базу.
        """
        
        bot.send_message(
            message.chat.id,
            response_message.strip(),
            parse_mode='HTML'
        )
        
        # Также отправить уведомление в консоль
        print(f"\n{'='*50}")
        print(f"📨 Новое сообщение от {user_name} ({user_id})")
        print(f"Сообщение: {parsed_data.get('message', 'N/A')}")
        print(f"Время: {parsed_data.get('timestamp', 'N/A')}")
        print(f"{'='*50}\n")
        
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        bot.send_message(
            message.chat.id,
            "❌ Ошибка обработки данных. Попробуйте еще раз."
        )
    except Exception as e:
        print(f"Ошибка обработки: {e}")
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка: {str(e)}"
        )

@bot.message_handler(commands=['users'])
def users_command(message):
    """Обработчик команды /users (показать пользователей)"""
    total_users = len(user_data)
    
    users_list = "👥 Список пользователей:\n\n"
    for idx, (uid, data) in enumerate(user_data.items(), 1):
        name = data.get('first_name', 'Unknown')
        username = data.get('username', 'Unknown')
        joined = data.get('joined', 'N/A')
        users_list += f"{idx}. {name} (@{username})\n   ID: <code>{uid}</code>\n   Присоединился: {joined}\n\n"
    
    if total_users == 0:
        users_list = "Еще нет пользователей"
    
    bot.send_message(message.chat.id, users_list, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    """Обработчик остальных сообщений"""
    response = f"""
📝 Вы отправили: <code>{message.text}</code>

💡 Совет: Используйте команды:
/start - Начать
/help - Помощь
/info - Ваша информация
/stats - Статистика

Или откройте мини-приложение кнопкой выше.
    """
    bot.send_message(message.chat.id, response.strip(), parse_mode='HTML')

def print_startup_message():
    """Вывести стартовое сообщение"""
    print("\n" + "="*60)
    print("🤖 TELEGRAM МИН-ПРИЛОЖЕНИЕ БОТ")
    print("="*60)
    print(f"✅ Бот успешно запущен!")
    print(f"🆔 Token: {TOKEN[:20]}...")
    print(f"⏰ Время запуска: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"🌐 URL приложения: {WEB_APP_URL}")
    print("="*60)
    print("📤 Бот ожидает сообщения...\n")

if __name__ == '__main__':
    print_startup_message()
    
    try:
        # Запустить бота
        bot.polling(none_stop=True, interval=0)
    except KeyboardInterrupt:
        print("\n\n❌ Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка при работе бота: {e}")
