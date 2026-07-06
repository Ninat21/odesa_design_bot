# Таблиця `user_interests`

## Призначення

Зв'язок між користувачем та його інтересами.

---

# Поля

| Поле | Тип |
|------|-----|
| id | BIGSERIAL |
| user_id | BIGINT |
| interest_id | BIGINT |
| source | VARCHAR(50) |
| confidence | NUMERIC(5,2) |
| verified | BOOLEAN |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

# Обмеження

```
UNIQUE(user_id, interest_id)
```