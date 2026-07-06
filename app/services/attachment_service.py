from aiogram.types import Message

from app.database.models import Message as DBMessage
from app.database.repositories.message_attachments import (
    MessageAttachmentRepository,
)


class AttachmentService:
    def __init__(
        self,
        attachments: MessageAttachmentRepository,
    ):
        self.attachments = attachments

    async def save_attachments(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ) -> None:

        if telegram_message.photo:
            await self._save_photo(
                telegram_message,
                db_message,
            )

        if telegram_message.document:
            await self._save_document(
                telegram_message,
                db_message,
            )

        if telegram_message.video:
            await self._save_video(
                telegram_message,
                db_message,
            )

        if telegram_message.audio:
            await self._save_audio(
                telegram_message,
                db_message,
            )

        if telegram_message.voice:
            await self._save_voice(
                telegram_message,
                db_message,
            )

        if telegram_message.animation:
            await self._save_animation(
                telegram_message,
                db_message,
            )

        if telegram_message.video_note:
            await self._save_video_note(
                telegram_message,
                db_message,
            )

        if telegram_message.sticker:
            await self._save_sticker(
                telegram_message,
                db_message,
            )

    async def _save_photo(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ):

        photo = max(
            telegram_message.photo,
            key=lambda p: p.file_size or 0,
        )

        await self.attachments.create(
            message_id=db_message.id,
            attachment_type="photo",
            telegram_file_id=photo.file_id,
            telegram_unique_file_id=photo.file_unique_id,
            file_size=photo.file_size,
            width=photo.width,
            height=photo.height,
        )

    async def _save_document(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ):

        document = telegram_message.document

        await self.attachments.create(
            message_id=db_message.id,
            attachment_type="document",
            telegram_file_id=document.file_id,
            telegram_unique_file_id=document.file_unique_id,
            file_name=document.file_name,
            mime_type=document.mime_type,
            file_size=document.file_size,
            thumbnail_file_id=(
                document.thumbnail.file_id
                if document.thumbnail
                else None
            ),
        )

    async def _save_video(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ):

        video = telegram_message.video

        await self.attachments.create(
            message_id=db_message.id,
            attachment_type="video",
            telegram_file_id=video.file_id,
            telegram_unique_file_id=video.file_unique_id,
            mime_type=video.mime_type,
            file_name=video.file_name,
            file_size=video.file_size,
            width=video.width,
            height=video.height,
            duration=video.duration,
            thumbnail_file_id=(
                video.thumbnail.file_id
                if video.thumbnail
                else None
            ),
        )

    async def _save_audio(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ):

        audio = telegram_message.audio

        await self.attachments.create(
            message_id=db_message.id,
            attachment_type="audio",
            telegram_file_id=audio.file_id,
            telegram_unique_file_id=audio.file_unique_id,
            file_name=audio.file_name,
            mime_type=audio.mime_type,
            file_size=audio.file_size,
            duration=audio.duration,
            thumbnail_file_id=(
                audio.thumbnail.file_id
                if audio.thumbnail
                else None
            ),
        )

    async def _save_voice(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ):

        voice = telegram_message.voice

        await self.attachments.create(
            message_id=db_message.id,
            attachment_type="voice",
            telegram_file_id=voice.file_id,
            telegram_unique_file_id=voice.file_unique_id,
            mime_type=voice.mime_type,
            file_size=voice.file_size,
            duration=voice.duration,
        )

    async def _save_animation(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ):

        animation = telegram_message.animation

        await self.attachments.create(
            message_id=db_message.id,
            attachment_type="animation",
            telegram_file_id=animation.file_id,
            telegram_unique_file_id=animation.file_unique_id,
            file_name=animation.file_name,
            mime_type=animation.mime_type,
            file_size=animation.file_size,
            width=animation.width,
            height=animation.height,
            duration=animation.duration,
            thumbnail_file_id=(
                animation.thumbnail.file_id
                if animation.thumbnail
                else None
            ),
        )

    async def _save_video_note(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ):

        note = telegram_message.video_note

        await self.attachments.create(
            message_id=db_message.id,
            attachment_type="video_note",
            telegram_file_id=note.file_id,
            telegram_unique_file_id=note.file_unique_id,
            file_size=note.file_size,
            width=note.length,
            height=note.length,
            duration=note.duration,
            thumbnail_file_id=(
                note.thumbnail.file_id
                if note.thumbnail
                else None
            ),
        )

    async def _save_sticker(
        self,
        telegram_message: Message,
        db_message: DBMessage,
    ):

        sticker = telegram_message.sticker

        await self.attachments.create(
            message_id=db_message.id,
            attachment_type="sticker",
            telegram_file_id=sticker.file_id,
            telegram_unique_file_id=sticker.file_unique_id,
            file_size=sticker.file_size,
            width=sticker.width,
            height=sticker.height,
            thumbnail_file_id=(
                sticker.thumbnail.file_id
                if sticker.thumbnail
                else None
            ),
        )