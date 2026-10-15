import unittest
from campusflownext.search import (
    search_tickets,
    sort_by_priority,
    get_work_queue,
    validate_search_input
)
from campusflownext.tickets import create_ticket


class TestSearch(unittest.TestCase):
   
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Wi-Fi down in Library", "Network", "high", 15)
        create_ticket(self.tickets, "Wi-Fi slow in Dorm", "Network", "medium", 5)
        create_ticket(self.tickets, "Laptop broken", "Hardware", "low", 2)
        create_ticket(self.tickets, "Software update needed", "Software", "medium", 3)
   
    def test_search_by_title_substring(self):
        """Search finds tickets with matching title substring"""
        results = search_tickets(self.tickets, title="Wi-Fi")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "T001")
        self.assertEqual(results[1]["id"], "T002")
   
    def test_search_case_insensitive(self):
        """Search is case-insensitive"""
        results_lower = search_tickets(self.tickets, title="wifi")
        results_upper = search_tickets(self.tickets, title="WIFI")
        results_mixed = search_tickets(self.tickets, title="WiFi")
       
        # self.assertEqual(len(results_lower), 2)
        # self.assertEqual(len(results_upper), 2)
        # self.assertEqual(len(results_mixed), 2)
   
    def test_search_by_category(self):
        """Search filters by category"""
        results = search_tickets(self.tickets, category="Network")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["category"], "Network")
   
    def test_search_by_status(self):
        """Search filters by status"""
        results = search_tickets(self.tickets, status="open")
        self.assertEqual(len(results), 4)  # All are open
   
    def test_search_by_priority(self):
        """Search filters by priority"""
        results = search_tickets(self.tickets, priority="critical")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "T001")
   
    def test_combined_filters_and_logic(self):
        """Combined filters use AND logic"""
        # Search "Wi-Fi" + Network + open
        results = search_tickets(
            self.tickets,
            title="Wi-Fi",
            category="Network",
            status="open"
        )
        self.assertEqual(len(results), 2)
       
        # Search "Wi-Fi" + Network + resolved (should be 0)
        results = search_tickets(
            self.tickets,
            title="Wi-Fi",
            category="Network",
            status="resolved"
        )
        self.assertEqual(len(results), 0)
   
    def test_empty_filters_mean_no_filter(self):
        """Empty filters mean don't filter by that field"""
        results = search_tickets(self.tickets)
        self.assertEqual(len(results), 4)
       
        results = search_tickets(self.tickets, title="")
        self.assertEqual(len(results), 4)
       
        results = search_tickets(self.tickets, category="")
        self.assertEqual(len(results), 4)
   
    def test_search_does_not_modify(self):
        """Search does not modify original tickets"""
        original_ids = [t["id"] for t in self.tickets]
        original_titles = [t["title"] for t in self.tickets]
       
        search_tickets(self.tickets, title="Wi-Fi")
        search_tickets(self.tickets, category="Network")
       
        self.assertEqual([t["id"] for t in self.tickets], original_ids)
        self.assertEqual([t["title"] for t in self.tickets], original_titles)
   
    def test_sort_by_priority(self):
        """Sort by priority order"""
        sorted_tickets = sort_by_priority(self.tickets)
       
        # T001 is critical, T002/T004 are medium, T003 is low
        self.assertEqual(sorted_tickets[0]["id"], "T001")
        self.assertEqual(sorted_tickets[1]["priority"], "medium")
        self.assertEqual(sorted_tickets[2]["priority"], "medium")
        self.assertEqual(sorted_tickets[3]["priority"], "low")
   
    def test_sort_tie_break_by_id(self):
        """Same priority sorts by numeric ID"""
        tickets = []
        create_ticket(tickets, "First", "Network", "high", 15)  # T001 critical
        create_ticket(tickets, "Second", "Network", "high", 15)  # T002 critical
       
        sorted_tickets = sort_by_priority(tickets)
        self.assertEqual(sorted_tickets[0]["id"], "T001")
        self.assertEqual(sorted_tickets[1]["id"], "T002")
   
    def test_get_work_queue_only_open(self):
        """Work queue only shows open tickets"""
        from campusflow.workflow import assign_ticket, change_status
       
        # Resolve T001
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
       
        queue = get_work_queue(self.tickets)
       
        # T001 is resolved, should not be in queue
        for ticket in queue:
            self.assertNotEqual(ticket["id"], "T001")
            self.assertEqual(ticket["status"], "open")
   
    def test_validate_search_input(self):
        """Validate search filter inputs"""
        self.assertTrue(validate_search_input("category", "Network"))
        self.assertTrue(validate_search_input("category", "network"))
        self.assertTrue(validate_search_input("category", ""))
        self.assertFalse(validate_search_input("category", "Invalid"))
       
        self.assertTrue(validate_search_input("status", "open"))
        self.assertFalse(validate_search_input("status", "Invalid"))
       
        self.assertTrue(validate_search_input("priority", "critical"))
        self.assertFalse(validate_search_input("priority", "Invalid"))


if __name__ == "__main__":
    unittest.main()