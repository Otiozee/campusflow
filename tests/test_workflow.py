import unittest
from campusflow.workflow import assign_ticket, change_status
from campusflow.tickets import create_ticket

class TestAssignment(unittest.TestCase):
    
    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(
           
            self.tickets, "Wi-Fi down", "Network", "high", 15
        )
    
    def test_assign_ticket(self):
        """Assign ticket to staff member"""
        result = assign_ticket(self.tickets, "T001", "Alice")
        self.assertEqual(result["assigned_to"], "Alice")
    
    def test_assign_unknown_ticket(self):
        """Unknown ticket ID should raise ValueError"""
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Alice")
    
    def test_assign_blank_staff(self):
        """Blank staff name should raise ValueError"""
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")


class TestStatusWorkflow(unittest.TestCase):
    
    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(
            self.tickets, "Wi-Fi down", "Network", "high", 15
        )
    
    def test_unassigned_cannot_start(self):
        """Unassigned ticket cannot move to in_progress"""
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")
    
    def test_assigned_can_progress(self):
        """Assigned ticket can go open → in_progress → resolved"""
        assign_ticket(self.tickets, "T001", "Alice")
        
        change_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.ticket["status"], "in_progress")
        
        change_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.ticket["status"], "resolved")
    
    def test_reopen_resolved(self):
        """Resolved ticket can be reopened to open"""
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        
        change_status(self.tickets, "T001", "open")
        self.assertEqual(self.ticket["status"], "open")
    
    def test_invalid_transition(self):
        """Cannot go from in_progress back to open, and state stays unchanged."""
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        before = [dict(ticket) for ticket in self.tickets]

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "open")
        self.assertEqual(self.tickets, before)


class TestWorkQueue(unittest.TestCase):
    
    def setUp(self):
        self.tickets = []
    
    def test_queue_sorted_by_priority(self):
        """Queue sorts by priority then ID"""
        # Create tickets with different priorities
        create_ticket(self.tickets, "Low issue", "Other", "low", 1)  # low
        create_ticket(self.tickets, "Critical issue", "Network", "high", 15)  # critical
        create_ticket(self.tickets, "Medium issue", "Software", "medium", 3)  # medium
        
        from campusflow.reports import get_work_queue
        queue = get_work_queue(self.tickets)
        
        self.assertEqual(queue[0]["priority"], "critical")
        self.assertEqual(queue[1]["priority"], "medium")
        self.assertEqual(queue[2]["priority"], "low")
    
    def test_queue_tie_break_by_id(self):
        """Same priority sorts by numeric ID"""
        create_ticket(self.tickets, "First", "Network", "high", 15)  # T001
        create_ticket(self.tickets, "Second", "Network", "high", 15)  # T002
        
        from campusflow.reports import get_work_queue
        queue = get_work_queue(self.tickets)
        
        self.assertEqual(queue[0]["id"], "T001")
        self.assertEqual(queue[1]["id"], "T002")

if __name__ == "__main__":
    unittest.main()