import json
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert

from app.database.database import SessionLocal
from app.database.models import Message, User

BATCH_SIZE = 500


def parse_text(text):

    if isinstance(text, str):
        return text

    if isinstance(text, list):

        result = ""

        for part in text:

            if isinstance(part, str):
                result += part

            elif isinstance(part, dict):
                result += part.get("text", "")

        return result

    return ""


def import_telegram_json(path: str):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    imported_messages = 0

    users = {}

    messages_batch = []

    for item in data["messages"]:

        if item.get("type") != "message":
            continue

        from_id = item.get("from_id")

        if not from_id:
            continue

        telegram_id = int(from_id.replace("user", ""))

        users[telegram_id] = {
            "telegram_id": telegram_id,
            "username": None,
            "first_name": item.get("from"),
            "last_name": None,
        }

        messages_batch.append(
            {
                "message_id": item["id"],
                "telegram_id": telegram_id,
                "chat_id": data["id"],
                "thread_id": None,
                "reply_to_message_id": item.get("reply_to_message_id"),
                "date": datetime.fromisoformat(item["date"]),
                "edit_date": None,
                "message_type": "text",
                "text": parse_text(item.get("text", "")),
                "caption": None,
                "has_photo": False,
                "has_video": False,
                "has_document": False,
                "has_voice": False,
                "has_audio": False,
                "has_animation": False,
                "has_sticker": False,
                "has_poll": False,
                "has_location": False,
                "has_contact": False,
            }
        )

    with SessionLocal() as session:

        stmt = insert(User).values(list(users.values()))
        stmt = stmt.on_conflict_do_nothing(index_elements=["telegram_id"])
        session.execute(stmt)

        for i in range(0, len(messages_batch), BATCH_SIZE):

            batch = messages_batch[i : i + BATCH_SIZE]

            stmt = insert(Message).values(batch)

            stmt = stmt.on_conflict_do_nothing(constraint="uq_chat_message")

            session.execute(stmt)

            print(
                f"Импортировано {min(i + BATCH_SIZE, len(messages_batch))} сообщений..."
            )

        session.commit()

    return {
        "users": len(users),
        "messages": len(messages_batch),
    }
