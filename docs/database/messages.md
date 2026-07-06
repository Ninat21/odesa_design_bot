# Таблиця `messages`

## Призначення

Таблиця `messages` містить усі повідомлення, отримані із Telegram.

Вона є одним із головних джерел даних для:

- аналітики;
- AI-аналізу;
- Knowledge Base;
- пошуку;
- статистики;
- побудови соціального графа.

Кожне повідомлення зберігається лише один раз.

---

# Відповідальність

Таблиця відповідає лише за фактичні дані повідомлення.

Вона не містить:

- AI-аналіз;
- реакції;
- вкладення;
- посилання;
- згадки;
- ембедінги.

Ці дані знаходяться в окремих таблицях.

---

# Поля

| Поле | Тип | NULL | Опис |
|------|-----|------|------|
| id | BIGSERIAL | ❌ | Внутрішній ідентифікатор |
| telegram_message_id | BIGINT | ❌ | ID повідомлення в Telegram |
| user_id | BIGINT | ❌ | Автор повідомлення |
| chat_id | BIGINT | ❌ | Telegram Chat ID |
| thread_id | BIGINT | ✅ | ID теми |
| reply_to_message_id | BIGINT | ✅ | Відповідь на повідомлення |
| forwarded_from_user_id | BIGINT | ✅ | Автор пересланого повідомлення |
| forwarded_chat_id | BIGINT | ✅ | Канал або чат пересилання |
| message_type | VARCHAR(30) | ❌ | Тип повідомлення |
| text | TEXT | ✅ | Текст повідомлення |
| caption | TEXT | ✅ | Підпис до медіа |
| telegram_date | TIMESTAMP | ❌ | Дата повідомлення в Telegram |
| edited_at | TIMESTAMP | ✅ | Дата редагування |
| deleted_at | TIMESTAMP | ✅ | Дата видалення (якщо відома) |
| views_count | INTEGER | ✅ | Кількість переглядів |
| forwards_count | INTEGER | ✅ | Кількість пересилань |
| created_at | TIMESTAMP | ❌ | Створення запису |
| updated_at | TIMESTAMP | ❌ | Останнє оновлення |

---

# Первинний ключ

```
id
```

---

# Зовнішні ключі

```
user_id → users.id

reply_to_message_id → messages.id
```

---

# Унікальність

У Telegram ID повідомлення унікальний лише в межах одного чату.

Тому використовується обмеження:

```
UNIQUE(chat_id, telegram_message_id)
```

---

# Типи повідомлень

Підтримуються:

- text
- photo
- video
- animation
- audio
- voice
- video_note
- sticker
- document
- contact
- location
- venue
- poll
- dice
- invoice
- service

---

# Індекси

Створюються індекси:

```
user_id

chat_id

telegram_date

message_type

reply_to_message_id

thread_id
```

---

# Зв'язки

## Один до одного

MessageAI

---

## Один до багатьох

MessageAttachments

MessageReactions

MessageMentions

MessageLinks

KnowledgeSources

---

# Правила оновлення

Після створення повідомлення дозволяється оновлювати лише:

- edited_at
- text
- caption
- updated_at

Інші поля повинні залишатися незмінними.

---

# Видалення

Фізичне видалення повідомлення не використовується.

Якщо Telegram повідомляє про видалення, встановлюється:

```
deleted_at
```

---

# Джерела даних

Допустимі джерела:

- Telegram Bot
- Telethon
- Import

AI не має права змінювати дані повідомлення.

---

# Причини такої структури

Повідомлення є основною одиницею інформації.

Усі додаткові дані винесені в окремі таблиці.

Це дозволяє:

- швидше виконувати пошук;
- зменшити розмір таблиці;
- не дублювати інформацію;
- спростити AI-аналіз.

---

# Майбутній розвиток

Можливе додавання:

- міток модерації;
- ознаки закріпленого повідомлення;
- інформації про автоматичні повідомлення;
- статусу архівації.