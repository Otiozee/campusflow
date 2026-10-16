
import unittest

from campusflow.tickets import create_ticket
from campusflow.notes import add_note


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(
            self.tickets,
            "Wi-Fi is down",
            "Network",
            "high",
            5,
        )

    def add_note(self, author="Samuel", message="Checked the network connection."):
        return add_note(
            self.tickets,
            self.ticket["id"],
            author,
            message,
        )

    def test_add_valid_note(self):
        """A valid note is saved with its author and message."""
        self.add_note()

        notes = self.ticket["notes"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["author"], "Samuel")
        self.assertEqual(notes[0]["message"], "Checked the network connection.")

    def test_note_message_is_trimmed(self):
        """Leading and trailing spaces are removed."""
        self.add_note(message="  Checked the network connection.  ")

        self.assertEqual(
            self.ticket["notes"][0]["message"],
            "Checked the network connection.",
        )

    def test_reject_invalid_author_or_message(self):
        """Blank authors and messages outside the allowed length are rejected."""
        invalid_cases = [
            ("", "Valid message"),
            ("   ", "Valid message"),
            ("Samuel", ""),
            ("Samuel", "   "),
            ("Samuel", "Four"),
            ("Samuel", "x" * 301),
        ]

        for author, message in invalid_cases:
            with self.subTest(author=author, message_length=len(message)):
                with self.assertRaises(ValueError):
                    self.add_note(author=author, message=message)

                self.assertEqual(self.ticket["notes"], [])

    def test_reject_unknown_ticket(self):
        """A note cannot be added to a ticket that does not exist."""
        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                "T999",
                "Samuel",
                "Checked the network connection.",
            )

        self.assertEqual(self.ticket["notes"], [])

    def test_reject_note_on_resolved_ticket(self):
        """Resolved tickets cannot receive notes."""
        self.ticket["status"] = "resolved"

        with self.assertRaises(ValueError):
            self.add_note()

        self.assertEqual(self.ticket["notes"], [])

    def test_multiple_notes_are_preserved(self):
        """Adding a second note does not overwrite the first."""
        self.add_note(message="Checked the network connection.")
        self.add_note(message="Restarted the router successfully.")

        notes = self.ticket["notes"]
        self.assertEqual(len(notes), 2)
        self.assertEqual(
            notes[0]["message"],
            "Checked the network connection.",
        )
        self.assertEqual(
            notes[1]["message"],
            "Restarted the router successfully.",
        )


if __name__ == "__main__":
    unittest.main()
