from telethon.tl.custom.dialog import Dialog

from app.telethon.client import client


async def get_dialog(
    chat_id: int,
) -> Dialog | None:

    async for dialog in client.iter_dialogs():

        if dialog.id == chat_id:
            return dialog

    return None