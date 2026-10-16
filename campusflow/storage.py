import json
import os
from .validation import validate_ticket_collection

def save_tickets(tickets, filename="data/tickets.json"):

    validate_ticket_collection(tickets)

    directory = os.path.dirname(filename)

    if directory:
        os.makedirs(directory, exist_ok=True)

    temporary = filename + ".tmp"

    with open(temporary, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)

    os.replace(temporary, filename)

def load_tickets(filename="data/tickets.json"):

    if not os.path.exists(filename):

        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            tickets = json.load(f)

    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON in {filename}: {exc}") from exc
        
    except UnicodeDecodeError as exc:
        raise ValueError(f"Saved file {filename} is not valid UTF-8 text") from exc

    # Preserve older CampusFlow records created before notes were introduced.
    # Only the missing notes field is migrated; all other required fields are
    # still checked by validate_ticket_collection below.
    if isinstance(tickets, list):
        for ticket in tickets:
            if isinstance(ticket, dict) and "notes" not in ticket:
                ticket["notes"] = []

    validate_ticket_collection(tickets)
    return tickets