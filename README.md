# diary — дневник (Flask)

Учебный проект: Flask + Flask-SQLAlchemy, вход/регистрация и карточки дневника.

## Локальный запуск

```
pip install -r requirements.txt
python main.py
```

Открыть http://127.0.0.1:5000

Локально база — файл `instance/diary.db` (по умолчанию), на хостинге адрес базы
берётся из переменной окружения `DATABASE_URL`.

## Деплой

Хостинг: Render (веб-сервис, тариф free), база: Render Postgres.
Команда запуска: `gunicorn main:app --bind 0.0.0.0:$PORT`
