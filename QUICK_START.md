# Быстрый запуск проекта

## 1. Backend (Django)

```bash
# Активация виртуального окружения
.venv\Scripts\activate

# Переход в папку Django
cd vuln_machines

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Запуск сервера
python manage.py runserver
```

**Backend будет доступен:** `http://localhost:8000`

## 2. Frontend (Vue.js)

```bash
# Переход в папку Vue
cd vue-frontend

# Установка зависимостей
npm install

# Запуск сервера разработки
npm run serve
```

**Frontend будет доступен:** `http://localhost:8080`

## 3. Первый запуск

1. Откройте `http://localhost:8080`
2. Нажмите "Вход" → "Регистрация"
3. Создайте пользователя (admin или user)
4. Войдите в систему
5. Создайте первую машину

## Проблемы?

- **Backend не запускается:** Проверьте, что виртуальное окружение активировано
- **Frontend не запускается:** Убедитесь, что Node.js установлен
- **Ошибки 400:** Проверьте консоль браузера (F12)

Подробная инструкция в `README.md` 