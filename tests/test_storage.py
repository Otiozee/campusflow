import unittest
import tempfile
import os
import json
from campusflownext.storage import save_tickets, load_tickets, next_ticket_id
from campusflownext.tickets import create_ticket
from campusflownext.notes import add_note


class TestStorage(unittest.TestCase):
    
    def setUp(self):
        # Create temp directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, "test_tickets.json")
    
    def tearDown(self):
        # Clean up temp files
        if os.path.exists(self.filename):
            os.remove(self.filename)
        os.rmdir(self.temp_dir)
    
    def test_save_and_load(self):
        """Save tickets then load them back"""
        tickets = []
        create_ticket(tickets, "Wi-Fi down", "Network", "high", 15, )
        create_ticket(tickets, "Laptop broken", "Hardware", "medium", 3)
        
        save_tickets(tickets, self.filename)
        loaded = load_tickets(self.filename)
        
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["id"], "T001")
        self.assertEqual(loaded[1]["id"], "T002")
    
    def test_load_missing_file(self):
        """Missing file returns empty list"""
        result = load_tickets(os.path.join(self.temp_dir, "nonexistent.json"))
        self.assertEqual(result, [])
    
    def test_load_malformed_json(self):
        """Malformed JSON raises ValueError"""
        with open(self.filename, "w") as f:
            f.write("{not valid json")
        
        with self.assertRaises(ValueError):
            load_tickets(self.filename)
    
    def test_load_duplicate_ids_rejected(self):
        """Duplicate ticket IDs rejected"""
        tickets = [
            {
                "id": "T001",
                "title": "First",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
                "notes": []
            },
            {
                "id": "T001",  # Duplicate!
                "title": "Second",
                "category": "Network",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "open",
                "assigned_to": None,
                "notes": []
            }
        ]
        
        with open(self.filename, "w") as f:
            json.dump(tickets, f)
        
        with self.assertRaises(ValueError):
            load_tickets(self.filename)
    
    def test_load_invalid_ticket_rejected(self):
        """Invalid ticket data rejected"""
        tickets = [
            {
                "id": "T001",
                "title": "First",
                # missing category
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
                "notes": []
            }
        ]
        
        with open(self.filename, "w") as f:
            json.dump(tickets, f)
        
        with self.assertRaises(ValueError):
            load_tickets(self.filename)
    
    def test_save_and_load_preserves_notes(self):
        """Notes preserved through save and load"""
        tickets = []
        create_ticket(tickets, "Wi-Fi down", "Network", "high", 15)
        add_note(tickets, "T001", "Mentor A", "First note here")
        add_note(tickets, "T001", "Mentor B", "Second note here")
        
        save_tickets(tickets, self.filename)
        loaded = load_tickets(self.filename)
        
        self.assertEqual(len(loaded[0]["notes"]), 2)
        self.assertEqual(loaded[0]["notes"][0]["note_id"], "N001")
        self.assertEqual(loaded[0]["notes"][1]["note_id"], "N002")
    
    def test_unique_ids_after_reload(self):
        """IDs remain unique after save and reload"""
        tickets = []
        create_ticket(tickets, "First", "Network", "high", 15)
        create_ticket(tickets, "Second", "Network", "low", 1)
        
        save_tickets(tickets, self.filename)
        loaded = load_tickets(self.filename)
        
        # Create new ticket after reload
        create_ticket(loaded, "Third", "Software", "medium", 5)
        
        ids = [t["id"] for t in loaded]
        self.assertEqual(len(ids), len(set(ids)), "IDs should be unique")
        self.assertEqual(loaded[2]["id"], "T003")
    
    def test_next_ticket_id_empty(self):
        """Next ticket ID for empty list is T001"""
        result = next_ticket_id([])
        self.assertEqual(result, "T001")
    
    def test_next_ticket_id_after_reload(self):
        """Next ticket ID continues after reload"""
        tickets = []
        create_ticket(tickets, "First", "Network", "high", 15)
        create_ticket(tickets, "Second", "Network", "low", 1)
        
        save_tickets(tickets, self.filename)
        loaded = load_tickets(self.filename)
        
        result = next_ticket_id(loaded)
        self.assertEqual(result, "T003")
    
    def test_next_ticket_id_with_gaps(self):
        """Next ticket ID handles gaps in sequence"""
        tickets = [
            {
                "id": "T001",
                "title": "First",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
                "notes": []
            },
            {
                "id": "T005",  # Gap!
                "title": "Second",
                "category": "Network",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "open",
                "assigned_to": None,
                "notes": []
            }
        ]
        
        result = next_ticket_id(tickets)
        self.assertEqual(result, "T006")


if __name__ == "__main__":
    unittest.main()
