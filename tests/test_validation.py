import unittest
from campusflownext.validation import (
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    validate_staff_name,
    validate_note_author,
    validate_note_message,
    validate_ticket,
    can_transition
)


class TestValidation(unittest.TestCase):
    
    def test_valid_title(self):
        """Valid title passes"""
        result = validate_title("Wi-Fi down")
        self.assertEqual(result, "Wi-Fi down")
    
    def test_blank_title_rejected(self):
        """Blank title raises ValueError"""
        with self.assertRaises(ValueError):
            validate_title("   ")
    
    def test_valid_category(self):
        """Valid category passes"""
        result = validate_category("Network")
        self.assertEqual(result, "network")
    
    def test_invalid_category_rejected(self):
        """Invalid category raises ValueError"""
        with self.assertRaises(ValueError):
            validate_category("Invalid")
    
    def test_valid_urgency(self):
        """Valid urgency passes"""
        result = validate_urgency("HIGH")
        self.assertEqual(result, "high")
    
    def test_invalid_urgency_rejected(self):
        """Invalid urgency raises ValueError"""
        with self.assertRaises(ValueError):
            validate_urgency("urgent")
    
    def test_valid_affected_users(self):
        """Valid positive integer passes"""
        result = validate_affected_users(15)
        self.assertEqual(result, 15)
    
    def test_zero_affected_users_rejected(self):
        """Zero raises ValueError"""
        with self.assertRaises(ValueError):
            validate_affected_users(0)
    
    def test_negative_affected_users_rejected(self):
        """Negative raises ValueError"""
        with self.assertRaises(ValueError):
            validate_affected_users(-5)
    
    def test_float_affected_users_rejected(self):
        """Float raises ValueError"""
        with self.assertRaises(ValueError):
            validate_affected_users(5.5)
    
    def test_boolean_affected_users_rejected(self):
        """Boolean raises ValueError (bool is subclass of int)"""
        with self.assertRaises(ValueError):
            validate_affected_users(True)
    
    def test_string_affected_users_rejected(self):
        """String raises ValueError"""
        with self.assertRaises(ValueError):
            validate_affected_users("15")
    
    def test_valid_staff_name(self):
        """Valid staff name passes"""
        result = validate_staff_name("Alice")
        self.assertEqual(result, "Alice")
    
    def test_blank_staff_name_rejected(self):
        """Blank staff name raises ValueError"""
        with self.assertRaises(ValueError):
            validate_staff_name("   ")
    
    def test_valid_note_author(self):
        """Valid note author passes"""
        result = validate_note_author("Mentor A")
        self.assertEqual(result, "Mentor A")
    
    def test_blank_note_author_rejected(self):
        """Blank note author raises ValueError"""
        with self.assertRaises(ValueError):
            validate_note_author("")
    
    def test_valid_note_message(self):
        """Valid note message passes"""
        result = validate_note_message("Wi-Fi router reboot attempted")
        self.assertEqual(result, "Wi-Fi router reboot attempted")
    
    def test_short_note_message_rejected(self):
        """Message shorter than 5 chars raises ValueError"""
        with self.assertRaises(ValueError):
            validate_note_message("abc")
    
    def test_long_note_message_rejected(self):
        """Message longer than 300 chars raises ValueError"""
        with self.assertRaises(ValueError):
            validate_note_message("a" * 301)
    
    def test_can_transition_open_to_in_progress(self):
        """Open to in_progress with assignment is valid"""
        result = can_transition("open", "in_progress", "Alice")
        self.assertTrue(result)
    
    def test_can_transition_unassigned_to_in_progress(self):
        """Open to in_progress without assignment raises ValueError"""
        with self.assertRaises(ValueError):
            can_transition("open", "in_progress", None)
    
    def test_can_transition_resolved_to_open(self):
        """Resolved to open (reopen) is valid"""
        result = can_transition("resolved", "open", "Alice")
        self.assertTrue(result)
    
    def test_can_transition_invalid(self):
        """Invalid transition raises ValueError"""
        with self.assertRaises(ValueError):
            can_transition("in_progress", "open", "Alice")


class TestTicketValidation(unittest.TestCase):
    
    def test_valid_ticket(self):
        """Valid ticket passes validation"""
        ticket = {
            "id": "T001",
            "title": "Wi-Fi down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 15,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "notes": []
        }
        result = validate_ticket(ticket)
        self.assertEqual(result["id"], "T001")
    
    def test_missing_field_rejected(self):
        """Ticket missing required field raises ValueError"""
        ticket = {
            "id": "T001",
            "title": "Wi-Fi down",
            # missing category
            "urgency": "high",
            "affected_users": 15,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "notes": []
        }
        with self.assertRaises(ValueError):
            validate_ticket(ticket)
    
    def test_invalid_notes_rejected(self):
        """Ticket with invalid notes raises ValueError"""
        ticket = {
            "id": "T001",
            "title": "Wi-Fi down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 15,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "notes": [{"invalid": "note"}]
        }
        with self.assertRaises(ValueError):
            validate_ticket(ticket)


if __name__ == "__main__":
    unittest.main()
