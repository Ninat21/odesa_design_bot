from app.database import create_database
from app.services.importer import import_telegram_json


def main():

    create_database()

    result = import_telegram_json("result.json")

    print()
    print("========== ГОТОВО ==========")
    print(f"👥 Користувачів: {result['users']}")
    print(f"💬 Повідомлень: {result['messages']}")
    print("============================")


if __name__ == "__main__":
    main()