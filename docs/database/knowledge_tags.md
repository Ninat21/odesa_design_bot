# Таблиця `knowledge_tags`

## Призначення

Таблиця містить теги статей бази знань.

Теги використовуються для пошуку, фільтрації та групування матеріалів.

---

# Поля

| Поле | Тип | NULL | Опис |
|------|------|------|------|
| id | BIGSERIAL | ❌ | Первинний ключ |
| knowledge_article_id | BIGINT | ❌ | knowledge_articles.id |
| tag | VARCHAR(100) | ❌ | Назва тегу |
| created_at | TIMESTAMP | ❌ | Дата створення |

---

# Зовнішні ключі

```
knowledge_article_id → knowledge_articles.id
```

---

# Обмеження

```
UNIQUE(knowledge_article_id, tag)
```

---

# Індекси

```
tag

knowledge_article_id
```

---

# Причини такої структури

Теги дозволяють швидко знаходити матеріали за тематикою без побудови складної ієрархії категорій.