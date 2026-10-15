import json
import os
from campusflownext.validation import validate_ticket


def save_tickets(tickets, filename="data/tickets.json"):
    """
    Save tickets to JSON file.
    
    Args:
        tickets: list of ticket dictionaries
        filename: path to save file
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w") as f:
        json.dump(tickets, f, indent=2)


def load_tickets(filename="data/tickets.json"):
    """
    Load tickets from JSON file with full validation.
    
    Args:
        filename: path to load file
    
    Returns:
        List of tickets
    
    Raises:
        ValueError: if file is malformed or contains invalid data
    """
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, "r") as f:
            tickets = json.load(f)
        
        # Validate it's a list
        if not isinstance(tickets, list):
            raise ValueError("Ticket file must contain a list")
        
        # Validate each ticket
        for ticket in tickets:
            validate_ticket(ticket)
        
        # Check for duplicate IDs
        ticket_ids = [t["id"] for t in tickets]
        if len(ticket_ids) != len(set(ticket_ids)):
            raise ValueError("Duplicate ticket IDs found in file")
        
        # Check for duplicate note IDs within each ticket
        for ticket in tickets:
            note_ids = [n["note_id"] for n in ticket["notes"]]
            if len(note_ids) != len(set(note_ids)):
                raise ValueError(
                    f"Duplicate note IDs in ticket {ticket['id']}"
                )
        
        return tickets
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON in {filename}: {e}")


def next_ticket_id(tickets):
    """
    Calculate the next ticket ID based on existing tickets.
    
    Args:
        tickets: list of tickets
    
    Returns:
        String like "T001"
    """
    if not tickets:
        return "T001"
    
    # Find the max numeric ID
    max_num = 0
    for ticket in tickets:
        try:
            num = int(ticket["id"][1:])
            if num > max_num:
                max_num = num
        except (ValueError, IndexError):
            continue
    
    return f"T{max_num + 1:03d}"
