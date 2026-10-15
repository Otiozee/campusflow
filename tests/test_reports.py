import unittest
from campusflownext.reports import get_report, get_work_queue
from campusflownext.tickets import create_ticket
from campusflownext.workflow import assign_ticket, change_status


class TestReports(unittest.TestCase):
   
    def setUp(self):
        self.tickets = []
   
    def test_empty_report(self):
        """Empty report returns 0% without crash"""
        report = get_report(self.tickets)
       
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolved"], 0)
   
    def test_report_counts(self):
        """Report counts match known fixture"""
        create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 15)  # T001 critical
        create_ticket(self.tickets, "Laptop broken", "Hardware", "low", 2)  # T002 low
        create_ticket(self.tickets, "Software issue", "Software", "medium", 3)  # T003 medium
       
        report = get_report(self.tickets)
       
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_status"]["open"], 3)
        self.assertEqual(report["by_status"]["in_progress"], 0)
        self.assertEqual(report["by_status"]["resolved"], 0)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["medium"], 1)
        self.assertEqual(report["by_priority"]["low"], 1)
        self.assertEqual(report["by_category"]["Network"], 1)
        self.assertEqual(report["by_category"]["Hardware"], 1)
        self.assertEqual(report["by_category"]["Software"], 1)
        self.assertEqual(report["unresolved"], 3)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)
   
    def test_report_after_resolve(self):
        """Report counts after resolving a ticket"""
        create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 15)  # T001
        create_ticket(self.tickets, "Laptop broken", "Hardware", "low", 2)  # T002
       
        # Resolve T001
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
       
        report = get_report(self.tickets)
       
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["unresolved"], 1)
        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["resolution_percentage"], 50.0)
   
    def test_report_after_reopen(self):
        """Report counts after reopening a ticket"""
        create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 15)  # T001
       
        # Resolve then reopen
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        change_status(self.tickets, "T001", "open")
       
        report = get_report(self.tickets)
       
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["resolved"], 0)
        self.assertEqual(report["unresolved"], 1)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)
   
    def test_report_no_double_counting(self):
        """Report doesn't double-count tickets"""
        create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 15)
        create_ticket(self.tickets, "Laptop broken", "Hardware", "low", 2)
        create_ticket(self.tickets, "Software issue", "Software", "medium", 3)
       
        report = get_report(self.tickets)
       
        # Sum of statuses should equal total
        status_sum = sum(report["by_status"].values())
        self.assertEqual(status_sum, report["total"])
       
        # Sum of priorities should equal total
        priority_sum = sum(report["by_priority"].values())
        self.assertEqual(priority_sum, report["total"])
       
        # Sum of categories should equal total
        category_sum = sum(report["by_category"].values())
        self.assertEqual(category_sum, report["total"])
   
    def test_work_queue_only_open(self):
        """Work queue only shows open tickets"""
        create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 15)  # T001
        create_ticket(self.tickets, "Laptop broken", "Hardware", "low", 2)  # T002
       
        # Resolve T001
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
       
        queue = get_work_queue(self.tickets)
       
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["id"], "T002")
        self.assertEqual(queue[0]["status"], "open")
   
    def test_work_queue_sorted_by_priority(self):
        """Work queue sorted by priority"""
        create_ticket(self.tickets, "Low issue", "Other", "low", 1)  # T001 low
        create_ticket(self.tickets, "Critical issue", "Network", "high", 15)  # T002 critical
        create_ticket(self.tickets, "Medium issue", "Software", "medium", 3)  # T003 medium
       
        queue = get_work_queue(self.tickets)
       
        self.assertEqual(queue[0]["id"], "T002")  # critical
        self.assertEqual(queue[1]["id"], "T003")  # medium
        self.assertEqual(queue[2]["id"], "T001")  # low


if __name__ == "__main__":
    unittest.main()

