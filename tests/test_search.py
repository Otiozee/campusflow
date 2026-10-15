import unittest
from campusflow.search import search_titles

TICKETS = [
    {"id": "T001", "title": "Campus Wi-Fi is down", "category": "Network", "status": "open", "priority": "critical", "notes": []},
    {"id": "T002", "title": "Printer jammed", "category": "Hardware", "status": "in_progress", "priority": "medium", "notes": []},
    {"id": "T003", "title": "WiFi router rebooting", "category": "Network", "status": "resolved", "priority": "medium", "notes": []},
]


class TestSearchTitles(unittest.TestCase):
    def test_match_ignores_case(self):
        ids = [t["id"] for t in search_titles(TICKETS, "CAMPUS")]
        self.assertEqual(ids, ["T001"])

    def test_substring_match(self):
        ids = [t["id"] for t in search_titles(TICKETS, "jam")]
        self.assertEqual(ids, ["T002"])

    def test_blank_search_returns_all(self):
        self.assertEqual(len(search_titles(TICKETS, "   ")), 3)

    def test_no_match_returns_empty_list(self):
        self.assertEqual(search_titles(TICKETS, "zzz"), [])

    def test_results_are_copies(self):
        results = search_titles(TICKETS, "printer")
        results[0]["title"] = "changed"
        self.assertEqual(TICKETS[1]["title"], "Printer jammed")


if __name__ == "__main__":
    unittest.main()