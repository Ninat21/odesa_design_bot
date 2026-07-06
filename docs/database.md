# Database Architecture

Версия: 1.0

## Главные принципы

1. Факты никогда не смешиваются с выводами AI.
2. Любое изменение сохраняется.
3. Ничего не удаляется без причины.
4. Любое изменение имеет источник.
5. Любое изменение может быть восстановлено.
6. История сообщества важнее текущего состояния.

---

# Основные модули

## Identity

### users

Telegram-пользователь.

Хранит только объективные данные.

### profiles

Профиль, который пользователь заполняет самостоятельно.

### audit_log

История изменений любых данных.

---

## Community

### messages

Сообщения Telegram.

### message_attachments

Любые вложения.

### message_reactions

Реакции.

### message_mentions

Упоминания пользователей.

### message_links

Ссылки.

### message_ai

AI-анализ сообщений.

---

## AI

### ai_profiles

AI-профиль пользователя.

### ai_profile_history

История AI-профиля.

### ai_jobs

Очередь обработки AI.

### embeddings

Векторные представления.

---

## Events

### events

Все мероприятия.

### event_participants

Участники мероприятий.

### event_feedback

Отзывы.

---

## Organizations

### organizations

Компании.

### user_organizations

История работы.

---

## Projects

### projects

Проекты.

### project_participants

Участники.

### project_updates

История проекта.

---

## Reputation

### recommendations

Рекомендации.

### achievements

Справочник достижений.

### user_achievements

Полученные достижения.

### badges

Дополнительные награды.

---

## Knowledge

### knowledge

Карточки знаний.

### knowledge_sources

Сообщения-источники.

### knowledge_history

История знаний.

### faq

Частые вопросы.

---

## Timeline

### timeline

Все события жизни сообщества.

---

## System

### tags

Справочник тегов.

### tag_relations

Связи тегов.

### files

Метаданные файлов.

### settings

Настройки проекта.

### saved_searches

Сохранённые аналитические запросы.

### notifications

Очередь уведомлений.

### imports

История импортов.

### api_tokens

Внешние интеграции.

---

## Social Graph

### user_connections

Связи между участниками.

### interaction_events

Все взаимодействия пользователей.

---

## Будущие возможности

- AI-поиск специалистов.
- AI-память сообщества.
- Автоматическое обновление AI-профилей.
- Интеграция с Luma.
- Интеграция с сайтом сообщества.
- AI-рекомендации участников.
- Аналитика активности.
- Knowledge Base сообщества.