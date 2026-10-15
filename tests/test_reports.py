import unittest
from campusflow.reports import get_report

FIXTURE = [
    {"id": "T001", "category": "Network", "status": "open", "priority": "high"},
    {"id": "T002", "category": "Network", "status": "open", "priority": "low"},
    {"id": "T003", "category": "Hardware", "status": "resolved", "priority": "medium"},
]


class TestGetReport(unittest.TestCase):
    def test_empty_list_reports_zero_percent(self):
        report = get_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["resolution_percent"], 0.0)

    def test_counts_by_category(self):
        report = get_report(FIXTURE)
        self.assertEqual(report["by_category"]["Network"], 2)
        self.assertEqual(report["by_category"]["Hardware"], 1)

    def test_unresolved_and_resolved_counts(self):
        report = get_report(FIXTURE)
        self.assertEqual(report["unresolved"], 2)
        self.assertEqual(report["resolved"], 1)

    def test_resolution_percentage(self):
        report = get_report(FIXTURE)
        self.assertAlmostEqual(report["resolution_percent"], 33.33, places=2)

    def test_reopened_ticket_counts_as_unresolved(self):
        tickets = [dict(t) for t in FIXTURE]
        tickets[2]["status"] = "open"
        report = get_report(tickets)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["unresolved"], 3)


if __name__ == "__main__":
    unittest.main()