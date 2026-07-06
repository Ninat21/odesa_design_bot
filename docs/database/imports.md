# Таблиця `imports`

## Призначення

Таблиця містить історію всіх імпортів даних.

---

# Відповідальність

Таблиця відповідає за:

- журнал імпортів;
- контроль успішності;
- пошук помилок;
- повторний запуск.

---

# Поля

| Поле | Тип | NULL | Опис |
|------|------|------|------|
| id | BIGSERIAL | ❌ | Первинний ключ |
| source | VARCHAR(50) | ❌ | Джерело імпорту |
| file_name | VARCHAR(255) | ✅ | Назва файлу |
| status | VARCHAR(30) | ❌ | Статус |
| imported_users | INTEGER | ❌ | Імпортовано користувачів |
| imported_messages | INTEGER | ❌ | Імпортовано повідомлень |
| skipped_records | INTEGER | ❌ | Пропущено записів |
| error_message | TEXT | ✅ | Текст помилки |
| started_at | TIMESTAMP | ❌ | Початок |
| finished_at | TIMESTAMP | ✅ | Завершення |
| created_at | TIMESTAMP | ❌ | Створення |

---

# Статуси

- running
- completed
- failed
- cancelled

---

# Індекси

```
source

status

started_at
```

---

# Причини такої структури

Дозволяє бачити історію всіх імпортів та швидко знаходити причини помилок.