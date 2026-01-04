// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;

// Раскрыть приложение на полный размер
document.addEventListener('DOMContentLoaded', function() {
    // Включить режим расширения
    tg.expand();
    
    // Установить цвет фона приложения
    tg.setBackgroundColor('#ffffff');
    
    // Показать кнопку меню
    tg.MainButton.show();
    
    // Инициализировать приложение
    initializeApp();
    
    // Слушать событие изменения темы
    tg.onEvent('themeChanged', () => {
        updateTheme();
    });
});

// Функция инициализации приложения
function initializeApp() {
    try {
        // Получить информацию о пользователе
        const user = tg.initData ? JSON.parse(decodeURIComponent(tg.initData.split('user=')[1].split('&')[0])) : null;
        
        // Обновить приветствие
        const greeting = document.getElementById('greeting');
        if (user && user.first_name) {
            greeting.textContent = `Привет, ${user.first_name}! 👋`;
        } else {
            greeting.textContent = 'Добро пожаловать в тестовое приложение!';
        }
        
        // Обновить информацию о пользователе
        updateUserInfo(user);
        
        // Обновить информацию о теме
        updateTheme();
        
        // Установить обработчик главной кнопки
        tg.MainButton.text = '📤 Отправить данные';
        tg.MainButton.onClick(() => {
            sendData();
        });
        
    } catch (error) {
        console.error('Ошибка инициализации:', error);
        document.getElementById('status').textContent = 'Ошибка подключения';
    }
}

// Обновить информацию о пользователе
function updateUserInfo(user) {
    const status = document.getElementById('status');
    const userId = document.getElementById('userId');
    const userName = document.getElementById('userName');
    const userLanguage = document.getElementById('userLanguage');
    
    if (tg.initData) {
        status.textContent = '✅ Подключено';
        status.style.color = '#00aa00';
    } else {
        status.textContent = '⚠️ Тестовый режим';
        status.style.color = '#ff9800';
    }
    
    if (user) {
        userId.textContent = user.id || '-';
        userName.textContent = (user.first_name || '') + (user.last_name ? ' ' + user.last_name : '');
        userLanguage.textContent = user.language_code || 'не указан';
    } else {
        userId.textContent = 'Тестовый ID: 123456789';
        userName.textContent = 'Тестовый пользователь';
        userLanguage.textContent = 'ru';
    }
}

// Обновить тему приложения
function updateTheme() {
    const theme = document.getElementById('theme');
    
    if (tg.colorScheme === 'dark') {
        theme.textContent = '🌙 Темная';
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        theme.textContent = '☀️ Светлая';
        document.documentElement.removeAttribute('data-theme');
    }
    
    // Обновить цвета CSS переменных из Telegram
    const root = document.documentElement;
    
    if (tg.themeParams) {
        if (tg.themeParams.bg_color) {
            root.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color);
        }
        if (tg.themeParams.text_color) {
            root.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color);
        }
        if (tg.themeParams.hint_color) {
            root.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color);
        }
        if (tg.themeParams.link_color) {
            root.style.setProperty('--tg-theme-link-color', tg.themeParams.link_color);
        }
        if (tg.themeParams.button_color) {
            root.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color);
        }
        if (tg.themeParams.button_text_color) {
            root.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color);
        }
    }
}

// Показать уведомление
function showAlert() {
    tg.showAlert('✅ Это тестовое уведомление от приложения!');
}

// Показать подтверждение
function showConfirm() {
    tg.showConfirm('❓ Вы уверены?', (result) => {
        if (result) {
            tg.showAlert('✅ Вы подтвердили действие!');
        } else {
            tg.showAlert('❌ Вы отменили действие');
        }
    });
}

// Отправить данные боту
function sendData() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) {
        tg.showAlert('⚠️ Пожалуйста, введите сообщение');
        return;
    }
    
    // Отправить данные боту
    const data = {
        message: message,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent
    };
    
    // Отправить через веб-приложение
    tg.sendData(JSON.stringify(data));
    
    // Показать ответ
    const responseDiv = document.getElementById('responseMessage');
    const response = document.getElementById('response');
    response.textContent = `📨 Данные отправлены: "${message}"`;
    responseDiv.style.display = 'block';
    
    // Очистить входное поле
    input.value = '';
    
    // Скрыть ответ через 3 секунды
    setTimeout(() => {
        responseDiv.style.display = 'none';
    }, 3000);
}

// Закрыть приложение
function closeApp() {
    tg.showConfirm('❓ Вы хотите закрыть приложение?', (result) => {
        if (result) {
            tg.close();
        }
    });
}

// Логирование информации о приложении
console.log('Telegram Web App инициализирован');
console.log('Версия API:', tg.version);
console.log('Платформа:', tg.platform);
console.log('Цветовая схема:', tg.colorScheme);
console.log('ID приложения:', tg.initData);
