# Таблиця `user_skills`

## Призначення

Зберігає зв'язок між користувачем та його навичками.

---

# Поля

| Поле | Тип | NULL | Опис |
|------|-----|------|------|
| id | BIGSERIAL | ❌ | Первинний ключ |
| user_id | BIGINT | ❌ | users.id |
| skill_id | BIGINT | ❌ | skills.id |
| level | SMALLINT | ✅ | Рівень (1–5) |
| source | VARCHAR(50) | ❌ | Джерело |
| confidence | NUMERIC(5,2) | ✅ | Впевненість AI |
| verified | BOOLEAN | ❌ | Підтверджено користувачем |
| created_at | TIMESTAMP | ❌ | Створення |
| updated_at | TIMESTAMP | ❌ | Оновлення |

---

# Джерела

- user
- ai
- admin
- import

---

# Обмеження

```
UNIQUE(user_id, skill_id)
```