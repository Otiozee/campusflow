import unittest
from campusflow.tickets import calculate_priority, create_ticket

class TestPriorityCalculation(unittest.TestCase):
    
    def test_critical_high_urgency_10_users(self):
        """High urgency + 12 users = critical"""
        result = calculate_priority("high", 12)
        self.assertEqual(result, "critical")
    
    def test_high_urgency_few_users(self):
        """High urgency + 2 users = high"""
        result = calculate_priority("high", 2)
        self.assertEqual(result, "high")
    
    def test_medium_urgency_enough_users(self):
        """Low urgency + 4 users = medium (rule 3: >= 3 users)"""
        result = calculate_priority("low", 4)
        self.assertEqual(result, "medium")
    
    def test_low_priority_baseline(self):
        """Low urgency + 1 user = low"""
        result = calculate_priority("low", 1)
        self.assertEqual(result, "low")


class TestTicketCreation(unittest.TestCase):
    
    def setUp(self):
        """Create empty ticket list before each test"""
        self.tickets = []
    
    def test_create_valid_ticket(self):
        """Successfully create a ticket with valid inputs"""
        ticket = create_ticket(
            self.tickets,
            "Wi-Fi down",
            "Network",
            "high",
            15
        )
        
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(len(self.tickets), 1)
    
    def test_reject_zero_affected_users(self):
        """Zero affected users should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            create_ticket(self.tickets, "Test", "Network", "high", 0)
        
        self.assertIn("positive integer", str(context.exception))
    
    def test_reject_blank_title(self):
        """Blank title should raise ValueError"""
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "   ", "Network", "high", 5)
    
    def test_reject_invalid_category(self):
        """Invalid category should raise ValueError"""
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Test", "Invalid", "high", 5)
    
    def test_reject_invalid_urgency(self):
        """Invalid urgency should raise ValueError"""
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Test", "Network", "urgent", 5)
    
    def test_reject_decimal_affected_users(self):
        """Decimal affected_users should raise ValueError"""
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Test", "Network", "high", 5.5)
    
    def test_reject_boolean_affected_users(self):
        """Boolean affected_users should raise ValueError"""
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Test", "Network", "high", True)

    def test_invalid_create_leaves_collection_unchanged(self):
        """A rejected creation must not append or modify any ticket."""
        before = [dict(ticket) for ticket in self.tickets]
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Bad ticket", "Unknown", "high", 5)
        self.assertEqual(self.tickets, before)

if __name__ == "__main__":
    unittest.main()