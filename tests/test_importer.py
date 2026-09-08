from datetime import UTC, datetime
from unittest import TestCase

from app.services.importer import (
    analyze_membership_events,
    normalize_export_chat_id,
    parse_export_datetime,
    parse_text,
    parse_user_id,
)


class ImporterParserTest(TestCase):
    def test_parse_rich_text(self):
        value = ["Hello ", {"type": "bold", "text": "world"}, 10]
        self.assertEqual(parse_text(value), "Hello world")

    def test_parse_user_id(self):
        self.assertEqual(parse_user_id("user123"), 123)
        self.assertIsNone(parse_user_id("channel123"))
        self.assertIsNone(parse_user_id(None))

    def test_supergroup_chat_id_is_normalized_for_bot_api(self):
        self.assertEqual(
            normalize_export_chat_id(2_511_970_112, "private_supergroup"),
            -1_002_511_970_112,
        )
        self.assertEqual(normalize_export_chat_id(-1007, "supergroup"), -1007)

    def test_export_datetime_prefers_unix_timestamp(self):
        item = {
            "date": "2026-09-08T12:00:00",
            "date_unixtime": "1788858000",
        }
        self.assertEqual(
            parse_export_datetime(item),
            datetime.fromtimestamp(1_788_858_000, UTC),
        )

    def test_membership_events_use_reliable_ids_and_unique_aliases(self):
        messages = [
            {
                "type": "message",
                "from": "Invited User",
                "from_id": "user22",
                "date": "2026-09-02T12:00:00",
            },
            {
                "type": "service",
                "action": "join_group_by_link",
                "actor": "Link User",
                "actor_id": "user11",
                "date": "2026-09-03T12:00:00",
                "date_unixtime": "1788436800",
            },
            {
                "type": "service",
                "action": "invite_members",
                "actor": "Admin",
                "actor_id": "user1",
                "members": ["Invited User", "Unknown User"],
                "date": "2026-09-01T12:00:00",
                "date_unixtime": "1788264000",
            },
        ]

        result = analyze_membership_events(messages)

        self.assertEqual(result.link_events, 1)
        self.assertEqual(result.invite_references, 2)
        self.assertEqual(result.resolved_invites, 1)
        self.assertEqual(result.unmatched_invites, 1)
        self.assertEqual(set(result.joined_at_by_user), {11, 22})
        self.assertLess(
            result.joined_at_by_user[22],
            result.joined_at_by_user[11],
        )

    def test_ambiguous_member_name_is_not_guessed(self):
        messages = [
            {"type": "message", "from": "Same", "from_id": "user1"},
            {"type": "message", "from": "Same", "from_id": "user2"},
            {
                "type": "service",
                "action": "invite_members",
                "members": ["Same"],
                "date": "2026-09-01T12:00:00",
            },
        ]

        result = analyze_membership_events(messages)

        self.assertEqual(result.ambiguous_invites, 1)
        self.assertEqual(result.joined_at_by_user, {})

    def test_known_user_alias_can_resolve_silent_invited_member(self):
        messages = [
            {
                "type": "service",
                "action": "invite_members",
                "members": ["Silent User"],
                "date": "2026-09-01T12:00:00",
            },
        ]

        result = analyze_membership_events(
            messages,
            known_aliases={"Silent User": {77}},
        )

        self.assertEqual(result.resolved_invites, 1)
        self.assertEqual(set(result.joined_at_by_user), {77})

    def test_create_group_records_creator_and_initial_members(self):
        messages = [
            {
                "type": "service",
                "action": "create_group",
                "actor": "Creator",
                "actor_id": "user1",
                "members": ["Creator", "Founding Member"],
                "date": "2025-07-14T12:06:08",
                "date_unixtime": "1752483968",
            },
            {
                "type": "message",
                "from": "Founding Member",
                "from_id": "user2",
            },
        ]

        result = analyze_membership_events(messages)

        expected = datetime.fromtimestamp(1_752_483_968, UTC)
        self.assertEqual(result.joined_at_by_user, {1: expected, 2: expected})

    def test_self_leave_records_reliable_actor_id(self):
        messages = [
            {
                "type": "service",
                "action": "remove_members",
                "actor": "Former Member",
                "actor_id": "user42",
                "members": ["Former Member"],
                "date": "2026-09-01T12:00:00",
                "date_unixtime": "1788264000",
            }
        ]

        result = analyze_membership_events(messages)

        self.assertEqual(result.leave_events, 1)
        self.assertEqual(result.resolved_leaves, 1)
        self.assertEqual(
            result.left_at_by_user,
            {42: datetime.fromtimestamp(1_788_264_000, UTC)},
        )

    def test_admin_removal_uses_unique_member_alias(self):
        messages = [
            {"type": "message", "from": "Removed User", "from_id": "user77"},
            {
                "type": "service",
                "action": "remove_members",
                "actor": "Admin",
                "actor_id": "user1",
                "members": ["Removed User"],
                "date": "2026-09-01T12:00:00",
            },
        ]

        result = analyze_membership_events(messages)

        self.assertEqual(set(result.left_at_by_user), {77})
