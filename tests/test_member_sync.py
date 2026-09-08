from types import SimpleNamespace
from unittest import TestCase

from aiogram.enums import ChatMemberStatus

from app.services.member_sync import is_current_member


class MemberStatusTest(TestCase):
    def test_active_statuses_are_current_members(self):
        for status in (
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ):
            with self.subTest(status=status):
                self.assertTrue(is_current_member(SimpleNamespace(status=status)))

    def test_restricted_user_uses_is_member_flag(self):
        self.assertTrue(
            is_current_member(
                SimpleNamespace(
                    status=ChatMemberStatus.RESTRICTED,
                    is_member=True,
                )
            )
        )
        self.assertFalse(
            is_current_member(
                SimpleNamespace(
                    status=ChatMemberStatus.RESTRICTED,
                    is_member=False,
                )
            )
        )

    def test_left_user_is_not_current_member(self):
        self.assertFalse(
            is_current_member(SimpleNamespace(status=ChatMemberStatus.LEFT))
        )
