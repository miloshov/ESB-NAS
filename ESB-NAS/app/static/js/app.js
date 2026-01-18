// ESB-NAS Frontend JavaScript

// Translations
const translations = {
    en: {
        alert_title: "Emergency Alert System",
        alert_subtitle: "Select a template and press the button to send an alert",
        select_template: "Select Alert Template",
        alert_button: "ALERT!",
        sending: "Sending...",
        recipients_count: "Active Recipients",
        status_online: "System Online",
        language: "Language",
        theme: "Theme",
        dark: "Dark",
        light: "Light",
        admin_panel: "Admin Panel",
        logout: "Logout",
        login: "Login",
        username: "Username",
        password: "Password",
        login_button: "Sign In",
        templates: "Templates",
        recipients: "Recipients",
        integrations: "Integrations",
        test: "Test",
        settings: "Settings",
        logs: "Logs"
    },
    ua: {
        alert_title: "Система екстрених сповіщень",
        alert_subtitle: "Виберіть шаблон і натисніть кнопку для надсилання сповіщення",
        select_template: "Виберіть шаблон сповіщення",
        alert_button: "ТРИВОГА!",
        sending: "Надсилання...",
        recipients_count: "Активні одержувачі",
        status_online: "Система онлайн",
        language: "Мова",
        theme: "Тема",
        dark: "Темна",
        light: "Світла",
        admin_panel: "Панель адміністратора",
        logout: "Вихід",
        login: "Вхід",
        username: "Ім'я користувача",
        password: "Пароль",
        login_button: "Увійти",
        templates: "Шаблони",
        recipients: "Отримувачі",
        integrations: "Інтеграції",
        test: "Тест",
        settings: "Налаштування",
        logs: "Журнали"
    },
    sr: {
        alert_title: "Sistem za hitna obaveštenja",
        alert_subtitle: "Izaberite šablon i pritisnite dugme za slanje upozorenja",
        select_template: "Izaberite šablon upozorenja",
        alert_button: "ALERT!",
        sending: "Slanje...",
        recipients_count: "Aktivni primaoci",
        status_online: "Sistem online",
        language: "Jezik",
        theme: "Tema",
        dark: "Tamna",
        light: "Svetla",
        admin_panel: "Admin panel",
        logout: "Odjava",
        login: "Prijava",
        username: "Korisničko ime",
        password: "Lozinka",
        login_button: "Prijavi se",
        templates: "Šabloni",
        recipients: "Primaoci",
        integrations: "Integracije",
        test: "Test",
        settings: "Podešavanja",
        logs: "Logovi"
    },
    bg: {
        alert_title: "Система за спешни съобщения",
        alert_subtitle: "Изберете шаблон и натиснете бутона за изпращане на предупреждение",
        select_template: "Изберете шаблон за предупреждение",
        alert_button: "ТРЕВОГА!",
        sending: "Изпращане...",
        recipients_count: "Активни получатели",
        status_online: "Система онлайн",
        language: "Език",
        theme: "Тема",
        dark: "Тъмна",
        light: "Светла",
        admin_panel: "Административен панел",
        logout: "Изход",
        login: "Вход",
        username: "Потребителско име",
        password: "Парола",
        login_button: "Вход",
        templates: "Шаблони",
        recipients: "Получатели",
        integrations: "Интеграции",
        test: "Тест",
        settings: "Настройки",
        logs: "Дневници"
    }
};

// Current state
let currentLang = localStorage.getItem('language') || 'en';
let currentTheme = localStorage.getItem('theme') || 'dark';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Load saved preferences
    loadPreferences();
    
    // Setup language selector
    setupLanguageSelector();
    
    // Setup theme toggle
    setupThemeToggle();
    
    // Setup alert button
    setupAlertButton();
    
    // Setup modals
    setupModals();
});

// Load preferences
function loadPreferences() {
    // Apply theme
    if (currentTheme === 'dark') {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
    
    // Update theme button text
    const themeBtn = document.getElementById('theme-btn');
    if (themeBtn) {
        themeBtn.textContent = currentTheme === 'dark' ? translations[currentLang].light : translations[currentLang].dark;
    }
    
    // Update language buttons
    updateLanguageButtons();
}

// Setup language selector
function setupLanguageSelector() {
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const lang = this.dataset.lang;
            changeLanguage(lang);
        });
    });
}

function changeLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('language', lang);
    
    // Update all translatable elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (translations[lang] && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
    
    // Update form placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.dataset.i18nPlaceholder;
        if (translations[lang] && translations[lang][key]) {
            el.placeholder = translations[lang][key];
        }
    });
    
    // Update language buttons
    updateLanguageButtons();
    
    // Save to server
    fetch('/set-language', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: lang })
    });
}

function updateLanguageButtons() {
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => {
        if (btn.dataset.lang === currentLang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Setup theme toggle
function setupThemeToggle() {
    const themeBtn = document.getElementById('theme-btn');
    if (themeBtn) {
        themeBtn.addEventListener('click', toggleTheme);
    }
}

function toggleTheme() {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', currentTheme);
    
    if (currentTheme === 'dark') {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
    
    themeBtn.textContent = currentTheme === 'dark' ? translations[currentLang].light : translations[currentLang].dark;
    
    // Save to server
    fetch('/set-theme', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme: currentTheme })
    });
}

// Setup alert button
function setupAlertButton() {
    const alertBtn = document.getElementById('alert-btn');
    if (alertBtn) {
        alertBtn.addEventListener('click', sendAlert);
    }
}

async function sendAlert() {
    const templateSelect = document.getElementById('template-select');
    const templateId = templateSelect.value;
    
    if (!templateId) {
        showToast('Please select a template first!', 'error');
        return;
    }
    
    // Confirm before sending
    if (!confirm('Are you sure you want to send this alert? This action cannot be undone!')) {
        return;
    }
    
    const alertBtn = document.getElementById('alert-btn');
    const originalText = alertBtn.textContent;
    alertBtn.textContent = translations[currentLang].sending;
    alertBtn.disabled = true;
    
    try {
        const response = await fetch('/send-alert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ template_id: templateId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        showToast('Failed to send alert: ' + error.message, 'error');
    } finally {
        alertBtn.textContent = originalText;
        alertBtn.disabled = false;
    }
}

// Setup modals
function setupModals() {
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.modal').classList.remove('active');
        });
    });
    
    // Close modal on outside click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });
}

// Toast notifications
function showToast(message, type = 'success') {
    const container = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// Admin functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Form submissions
async function submitForm(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    
    try {
        const response = await fetch(form.action || window.location.href, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            closeModal(form.closest('.modal').id);
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        showToast('An error occurred: ' + error.message, 'error');
    }
}

// Delete confirmation
function confirmDelete(url, message = 'Are you sure?') {
    if (confirm(message)) {
        window.location.href = url;
    }
}

// Test integration
async function testIntegration(serviceType) {
    const testEmail = prompt('Enter test email (leave empty to skip email test):');
    const testPhone = prompt('Enter test phone number (leave empty to skip SMS test):');
    const testChatId = prompt('Enter Telegram chat ID (leave empty to skip Telegram test):');
    const testChannel = prompt('Enter Slack channel (leave empty to skip Slack test):');
    
    const formData = new FormData();
    formData.append('service_type', serviceType);
    if (testEmail) formData.append('test_email', testEmail);
    if (testPhone) formData.append('test_phone', testPhone);
    if (testChatId) formData.append('test_chat_id', testChatId);
    if (testChannel) formData.append('test_channel', testChannel);
    
    try {
        const response = await fetch('/admin/test', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        showToast('Test failed: ' + error.message, 'error');
    }
}
