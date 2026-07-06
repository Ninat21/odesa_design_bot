# Таблиця `skills`

## Призначення

Довідник професійних навичок.

Кожна навичка існує в системі лише один раз.

---

# Відповідальність

Таблиця містить перелік усіх професійних навичок.

Не містить інформації про користувачів.

---

# Поля

| Поле | Тип | NULL | Опис |
|------|-----|------|------|
| id | BIGSERIAL | ❌ | Первинний ключ |
| slug | VARCHAR(100) | ❌ | Унікальний ідентифікатор |
| name | VARCHAR(255) | ❌ | Назва навички |
| category | VARCHAR(100) | ✅ | Категорія |
| description | TEXT | ✅ | Опис |
| created_at | TIMESTAMP | ❌ | Створення |
| updated_at | TIMESTAMP | ❌ | Оновлення |

---

# Обмеження

```
UNIQUE(slug)
```

```
UNIQUE(name)
```

---

# Приклади

- Branding
- Packaging Design
- Typography
- UX Research
- Figma
- Blender
- Adobe Illustrator