# Таблиця `user_hobbies`

## Призначення

Зв'язок між користувачем та його хобі.

---

# Поля

| Поле | Тип |
|------|-----|
| id | BIGSERIAL |
| user_id | BIGINT |
| hobby_id | BIGINT |
| source | VARCHAR(50) |
| confidence | NUMERIC(5,2) |
| verified | BOOLEAN |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

# Обмеження

```
UNIQUE(user_id, hobby_id)
```