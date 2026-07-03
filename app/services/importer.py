import json
from datetime import datetime

from app.database.crud import add_message, add_user


def import_telegram_json(path: str):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    imported_users = set()
    imported_messages = 0

    for item in data["messages"]:

        if item["type"] != "message":
            continue

        if "from_id" not in item:
            continue

        telegram_id = int(item["from_id"].replace("user", ""))

        first_name = item.get("from", "")

        text = item.get("text", "")

        if isinstance(text, list):
            result = ""

            for part in text:

                if isinstance(part, str):
                    result += part

                elif isinstance(part, dict):
                    result += part.get("text", "")

            text = result

        add_user(
            telegram_id=telegram_id,
            username=None,
            first_name=first_name,
            last_name=None,
        )

        add_message(
            message_id=item["id"],
            telegram_id=telegram_id,
            chat_id=data["id"],
            date=datetime.fromisoformat(item["date"]),
            text=text,
        )

        imported_users.add(telegram_id)
        imported_messages += 1

    return {
        "users": len(imported_users),
        "messages": imported_messages,
    }