# Таблиця `users`

## Призначення

Таблиця `users` є центральною сутністю системи.

Вона містить лише фактичні дані про користувача, отримані з Telegram або внесені адміністраторами.

Таблиця не містить AI-висновків, соціальних зв'язків, навичок чи іншої похідної інформації.

---

# Відповідальність

Таблиця відповідає лише за:

- ідентифікацію користувача;
- членство у спільноті;
- технічну інформацію Telegram;
- статистичні лічильники;
- часові мітки активності.

---

# Поля

| Поле | Тип | NULL | Опис |
|------|-----|------|------|
| id | BIGSERIAL | ❌ | Внутрішній ідентифікатор |
| telegram_id | BIGINT | ❌ | Telegram ID |
| username | VARCHAR(255) | ✅ | Username |
| first_name | VARCHAR(255) | ✅ | Ім'я |
| last_name | VARCHAR(255) | ✅ | Прізвище |
| language_code | VARCHAR(10) | ✅ | Мова Telegram |
| is_bot | BOOLEAN | ❌ | Telegram Bot |
| is_premium | BOOLEAN | ❌ | Telegram Premium |
| is_member | BOOLEAN | ❌ | Поточний учасник спільноти |
| is_admin | BOOLEAN | ❌ | Адміністратор |
| is_banned | BOOLEAN | ❌ | Заблокований |
| joined_at | TIMESTAMP | ✅ | Дата вступу |
| left_at | TIMESTAMP | ✅ | Дата виходу |
| first_seen_at | TIMESTAMP | ✅ | Перша поява |
| last_seen_at | TIMESTAMP | ✅ | Остання поява |
| last_activity_at | TIMESTAMP | ✅ | Остання активність |
| last_message_at | TIMESTAMP | ✅ | Останнє повідомлення |
| messages_count | INTEGER | ❌ | Кількість повідомлень |
| media_count | INTEGER | ❌ | Кількість медіа |
| replies_count | INTEGER | ❌ | Кількість відповідей |
| created_at | TIMESTAMP | ❌ | Створення запису |
| updated_at | TIMESTAMP | ❌ | Останнє оновлення |

---

# Первинний ключ

```
id
```

Тип:

```
BIGSERIAL
```

---

# Унікальні поля

```
telegram_id
```

---

# Індекси

Створюються індекси:

```
telegram_id
username
is_member
last_activity_at
last_message_at
```

---

# Зв'язки

## Один до одного

```
Profile
```

```
AIProfile
```

---

## Один до багатьох

```
Messages
```

```
Timeline
```

```
AuditLog
```

```
Recommendations
```

```
EventParticipants
```

```
UserOrganizations
```

```
ProjectParticipants
```

```
UserAchievements
```

---

# Правила оновлення

`telegram_id`

Не змінюється.

---

`username`

Може змінюватися Telegram.

При зміні записується подія в Audit Log.

---

`first_name`

Може змінюватися.

---

`last_name`

Може змінюватися.

---

`joined_at`

Записується лише один раз.

---

`left_at`

Оновлюється після виходу користувача зі спільноти.

---

`messages_count`

Оновлюється автоматично.

Редагування вручну заборонене.

---

# Джерела даних

Допустимі джерела:

- Telegram Bot
- Telethon
- Administrator
- Import

AI не має права змінювати дані таблиці.

---

# Soft Delete

Фізичне видалення користувача не використовується.

Якщо користувач залишає спільноту:

```
is_member = false
left_at = NOW()
```

---

# Причини такої структури

Таблиця залишається максимально компактною.

Усі додаткові дані винесені в окремі сутності.

Це дозволяє:

- швидко виконувати пошук;
- швидко виконувати JOIN;
- уникати постійного додавання нових колонок.

---

# Майбутній розвиток

У майбутньому допускається додавання лише технічних полів.

Будь-які нові логічні сутності повинні створюватися в окремих таблицях.