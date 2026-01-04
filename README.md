# Telegram Mini App - Тестовое приложение

Это простое тестовое Telegram мини-приложение для изучения и разработки.

## 📋 Структура проекта

- **index.html** - основной HTML файл с структурой приложения
- **style.css** - стили и адаптивный дизайн
- **script.js** - логика приложения и интеграция с Telegram Web App API

## ✨ Возможности

- ✅ Полная интеграция с Telegram Web App SDK
- ✅ Отображение информации о пользователе
- ✅ Поддержка светлой и темной темы Telegram
- ✅ Уведомления и подтверждения
- ✅ Отправка данных боту
- ✅ Адаптивный дизайн (мобильные устройства)
- ✅ Отображение цветов темы приложения

## 🚀 Как использовать

### Локальное тестирование

1. Откройте файл `index.html` в браузере (локально приложение будет в режиме тестирования)
2. Протестируйте функциональность кнопок

### Развертывание на боте

1. Загрузите файлы на веб-сервер (например, GitHub Pages или собственный сервер)
2. Получите URL вашего приложения
3. Установите ссылку на приложение в боте Telegram через BotFather

**Команда BotFather:**
```
/setmenubutton
/setdefaultadministratorpermissions
/setbotcommands
```

## 🔧 Интеграция с ботом

Для полной интеграции создайте бота через [@BotFather](https://t.me/botfather) и добавьте обработчик веб-приложения:

**Пример на Python (pyTelegramBotAPI):**

```python
import telebot
from telebot import types

bot = telebot.TeleBot('YOUR_BOT_TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton(text="🚀 Открыть приложение", 
                               web_app=types.WebAppInfo(url="https://your-domain.com/index.html"))
    markup.add(btn)
    bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def web_app_data(message):
    data = message.web_app_data.data
    bot.send_message(message.chat.id, f"Данные получены: {data}")

bot.polling()
```

## 📱 Тестирование

### Способ 1: В браузере
- Откройте index.html в браузере
- Приложение будет в режиме тестирования

### Способ 2: В Telegram (требуется развертывание)
1. Создайте бота в BotFather
2. Установите веб-приложение
3. Нажмите на кнопку в чате

## 🎨 Теме и стилизация

Приложение автоматически подстраивается под тему Telegram пользователя:
- Светлая тема
- Темная тема
- Используются официальные цвета Telegram

## 📚 Документация

- [Telegram Web Apps Documentation](https://core.telegram.org/bots/webapps)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## ⚙️ Технологии

- HTML5
- CSS3 (с переменными CSS)
- Vanilla JavaScript
- Telegram Web App SDK

## 📝 Лицензия

MIT License

---

**Создано:** 4 января 2026 г.
**Версия:** 1.0
