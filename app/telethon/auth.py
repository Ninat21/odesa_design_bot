from telethon.errors import SessionPasswordNeededError

from app.config import Config
from app.telethon.client import client


async def authorize():
    if not Config.PHONE:
        raise RuntimeError("PHONE потрібен для першої авторизації Telethon")

    await client.connect()

    try:
        if not await client.is_user_authorized():

            await client.send_code_request(
                Config.PHONE,
            )

            code = input("Введіть код із Telegram: ")

            try:
                await client.sign_in(
                    Config.PHONE,
                    code,
                )

            except SessionPasswordNeededError:

                password = input(
                    "Введіть пароль двоетапної автентифікації: "
                )

                await client.sign_in(
                    password=password,
                )

        me = await client.get_me()

        print()
        print("=" * 50)
        print(f"Успішний вхід як: {me.first_name}")
        print(f"ID: {me.id}")
        print(f"Username: @{me.username}")
        print("=" * 50)

    finally:
        await client.disconnect()
