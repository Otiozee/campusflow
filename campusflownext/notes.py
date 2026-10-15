from campusflownext.validation import (
    validate_note_author,
    validate_note_message,
    validate_ticket_id
)
from campusflownext.tickets import find_ticket


def add_note(tickets, ticket_id, author, message):
    """
    Add a follow-up note to a ticket.
    
    Notes can only be added to open or in_progress tickets.
    Resolved tickets must be reopened first.
    
    Args:
        tickets: list of tickets
        ticket_id: string like "T001"
        author: non-blank string
        message: 5-300 characters
    
    Returns:
        The created note dictionary
    
    Raises:
        ValueError: if ticket not found, invalid inputs, or ticket resolved
    """
    # Validate inputs first
    valid_ticket_id = validate_ticket_id(ticket_id)
    valid_author = validate_note_author(author)
    valid_message = validate_note_message(message)
    
    # Find ticket
    ticket = find_ticket(tickets, valid_ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket {valid_ticket_id} not found")
    
    # Check status - only open or in_progress can accept notes
    if ticket["status"] == "resolved":
        raise ValueError(
            f"Cannot add note to resolved ticket {valid_ticket_id}. "
            "Reopen the ticket first."
        )
    
    # Generate note ID
    next_num = len(ticket["notes"]) + 1
    note_id = f"N{next_num:03d}"
    
    # Create note
    note = {
        "note_id": note_id,
        "author": valid_author,
        "message": valid_message
    }
    
    ticket["notes"].append(note)
    return note


def get_notes(tickets, ticket_id):
    """
    Get all notes for a ticket in ID order.
    
    Args:
        tickets: list of tickets
        ticket_id: string like "T001"
    
    Returns:
        List of notes
    
    Raises:
        ValueError: if ticket not found
    """
    valid_ticket_id = validate_ticket_id(ticket_id)
    
    ticket = find_ticket(tickets, valid_ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket {valid_ticket_id} not found")
    
    return ticket["notes"]


def next_note_id(ticket):
    """
    Calculate the next note ID for a ticket.
    
    Args:
        ticket: ticket dictionary
    
    Returns:
        String like "N001"
    """
    next_num = len(ticket["notes"]) + 1
    return f"N{next_num:03d}"
