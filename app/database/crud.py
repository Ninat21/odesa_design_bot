from sqlalchemy import func, select

from app.database.database import SessionLocal
from app.database.models import Message, User


def add_user(telegram_id, username, first_name, last_name):

    with SessionLocal() as session:

        user = session.get(User, telegram_id)

        if user is None:
            session.add(
                User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
            )

            session.commit()


def add_message(
    message_id,
    telegram_id,
    chat_id,
    date,
    text,
):

    with SessionLocal() as session:

        session.add(
            Message(
                message_id=message_id,
                telegram_id=telegram_id,
                chat_id=chat_id,
                date=date,
                text=text,
            )
        )

        session.commit()


def add_message_from_aiogram(message):

    add_message(
        message.message_id,
        message.from_user.id,
        message.chat.id,
        message.date,
        message.text,
    )


def get_stats():

    with SessionLocal() as session:

        users = session.scalar(
            select(func.count()).select_from(User)
        )

        messages = session.scalar(
            select(func.count()).select_from(Message)
        )

        return users, messages