from .workflow import find_ticket

def next_note_id(ticket):
    numbers = [int(n["note_id"][1:]) for n in ticket.get("notes", [])
               if isinstance(n.get("note_id"), str)
               and n["note_id"].startswith("N")
               and n["note_id"][1:].isdigit()]
    return f"N{max(numbers, default=0) + 1:03d}"

def add_note(tickets, ticket_id, author, message):
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} not found")
    if ticket["status"] not in ("open", "in_progress"):
        raise ValueError("Notes can only be added to open or in-progress tickets")
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be blank")
    if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
        raise ValueError("Note message must be 5–300 characters after trimming")
    note = {"note_id": next_note_id(ticket), "author": author.strip(), "message": message.strip()}
    ticket.setdefault("notes", []).append(note)
    return note

def get_notes(tickets, ticket_id):
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} not found")
    return sorted(ticket.get("notes", []), key=lambda n: int(n["note_id"][1:]))