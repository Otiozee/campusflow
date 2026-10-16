import unittest
from campusflownext.notes import add_note, get_notes, next_note_id
from campusflownext.tickets import create_ticket
from campusflownext.workflow import assign_ticket, change_status


class TestNotes(unittest.TestCase):
    
    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(
            self.tickets, "Wi-Fi down", "Network", "high", 15
        )
    
    def test_add_note_to_open_ticket(self):
        """Can add note to open ticket"""
        note = add_note(self.tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        
        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Mentor A")
        self.assertEqual(len(self.ticket["notes"]), 1)
    
    def test_add_second_note(self):
        """Second note gets N002"""
        add_note(self.tickets, "T001", "Mentor A", "First note here")
        note = add_note(self.tickets, "T001", "Mentor B", "Second note here")
        
        self.assertEqual(note["note_id"], "N002")
        self.assertEqual(len(self.ticket["notes"]), 2)
    
    def test_add_note_to_in_progress(self):
        """Can add note to in_progress ticket"""
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        
        note = add_note(self.tickets, "T001", "Mentor A", "Working on it now")
        
        self.assertEqual(note["note_id"], "N001")
    
    def test_add_note_to_resolved_rejected(self):
        """Cannot add note to resolved ticket"""
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor A", "This should fail")
        
        # Verify no note was added
        self.assertEqual(len(self.ticket["notes"]), 0)
    
    def test_add_note_after_reopen(self):
        """Can add note after reopening resolved ticket"""
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        change_status(self.tickets, "T001", "open")
        
        note = add_note(self.tickets, "T001", "Mentor A", "Reopened and adding note")
        
        self.assertEqual(note["note_id"], "N001")
    
    def test_blank_author_rejected(self):
        """Blank author raises ValueError"""
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "   ", "Valid message here")
        
        # Verify no note was added
        self.assertEqual(len(self.ticket["notes"]), 0)
    
    def test_short_message_rejected(self):
        """Message shorter than 5 chars raises ValueError"""
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor A", "abc")
        
        # Verify no note was added
        self.assertEqual(len(self.ticket["notes"]), 0)
    
    def test_rejected_note_does_not_consume_id(self):
        """Rejected note doesn't consume note ID"""
        # Try invalid note first
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor A", "abc")
        
        # Valid note should still get N001
        note = add_note(self.tickets, "T001", "Mentor A", "Valid message here")
        self.assertEqual(note["note_id"], "N001")
    
    def test_unknown_ticket_rejected(self):
        """Unknown ticket raises ValueError"""
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T999", "Mentor A", "Valid message here")
    
    def test_get_notes(self):
        """Get notes returns all notes in order"""
        add_note(self.tickets, "T001", "Mentor A", "First note here")
        add_note(self.tickets, "T001", "Mentor B", "Second note here")
        
        notes = get_notes(self.tickets, "T001")
        
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0]["note_id"], "N001")
        self.assertEqual(notes[1]["note_id"], "N002")
    
    def test_notes_preserved_through_resolve_reopen(self):
        """Notes preserved through resolve and reopen"""
        add_note(self.tickets, "T001", "Mentor A", "First note here")
        
        assign_ticket(self.tickets, "T001", "Alice")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        change_status(self.tickets, "T001", "open")
        
        notes = get_notes(self.tickets, "T001")
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["message"], "First note here")
    
    def test_next_note_id(self):
        """Next note ID calculation"""
        self.assertEqual(next_note_id(self.ticket), "N001")
        
        add_note(self.tickets, "T001", "Mentor A", "First note here")
        self.assertEqual(next_note_id(self.ticket), "N002")

    def test_note_id_does_not_collide_after_reload(self):
        """Note IDs don't collide after save and reload"""
        from campusflow.storage import save_tickets, load_tickets
        import tempfile, os
   
        # Create temp file
        temp_dir = tempfile.mkdtemp()
        filename = os.path.join(temp_dir, "test.json")
   
        # Add notes
        add_note(self.tickets, "T001", "Mentor A", "First note here")
        add_note(self.tickets, "T001", "Mentor B", "Second note here")

        # Save and reload
        save_tickets(self.tickets, filename)
        loaded = load_tickets(filename)

        # Add another note after reload
        note = add_note(loaded, "T001", "Mentor C", "Third note here")
   
        # Should get N003, not N001 again
        self.assertEqual(note["note_id"], "N003")
   
        # Clean up
        os.remove(filename)
        os.rmdir(temp_dir)



if __name__ == "__main__":
    unittest.main()
