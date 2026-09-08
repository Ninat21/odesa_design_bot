# Odesa Design Bot

Telegram-бот сообщества с PostgreSQL, SQLAlchemy, Alembic, Aiogram и утилитами
Telethon для импорта истории и участников.

## Локальный запуск

Требуется Python 3.13 и PostgreSQL.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Заполните `.env`, затем примените миграции и запустите бота:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe main.py
```

Обязательные переменные: `BOT_TOKEN`, `DATABASE_URL`, `GROUP_ID` и
`ADMIN_IDS`. Несколько Telegram ID администраторов указываются через запятую.
`HEALTH_PORT` необязателен и по умолчанию равен `8080`.

Для production достаточно зависимостей из `requirements.txt`.

## Проверки

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Интеграционные тесты требуют отдельную PostgreSQL-базу в
`TEST_DATABASE_URL`. Никогда не указывайте в этой переменной рабочую базу.
GitHub Actions автоматически создаёт одноразовую базу и выполняет полный набор
проверок.

## Импорт данных

Сначала один раз авторизуйте Telethon:

```powershell
.\.venv\Scripts\python.exe telethon_login.py
```

Доступные команды:

```powershell
# JSON-экспорт Telegram; без аргумента используется result.json
.\.venv\Scripts\python.exe import_history.py C:\path\to\result.json

# После JSON-импорта сверить статусы известных пользователей с Telegram
.\.venv\Scripts\python.exe sync_known_members.py

# История группы из GROUP_ID
.\.venv\Scripts\python.exe telethon_import_history.py

# Участники группы из GROUP_ID
.\.venv\Scripts\python.exe telethon_import_members.py
```

Файлы `.env`, `*.session`, Telegram-экспорты и локальная база исключены из Git.

## Сброс базы

Команда удаляет все прикладные таблицы и создаёт их заново:

```powershell
.\.venv\Scripts\python.exe reset_database.py --yes-i-really-mean-it
```

Для удалённой базы дополнительно требуется `ALLOW_DATABASE_RESET=1`. Перед
сбросом рабочей базы обязательно сделайте резервную копию.

Расширенная документация проекта находится в каталоге [`docs`](docs/README.md).
Инструкция по безопасному выпуску находится в
[`docs/deployment.md`](docs/deployment.md).
