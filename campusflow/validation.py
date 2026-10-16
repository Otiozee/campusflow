"""Shared validation rules for CampusFlow ticket records."""

CATEGORIES = ("Network", "Hardware", "Software", "Other")
URGENCIES = ("low", "medium", "high")
PRIORITIES = ("critical", "high", "medium", "low")
STATUSES = ("open", "in_progress", "resolved")
TICKET_FIELDS = {"id", "title", "category", "urgency", "affected_users",
                 "priority", "status", "assigned_to", "notes"}


def validate_ticket_fields(title, category, urgency, affected_users):

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be blank")

    if not isinstance(category, str) or category.strip().casefold() not in {c.casefold() for c in CATEGORIES}:
        raise ValueError(f"Invalid category: {category}")

    if not isinstance(urgency, str) or urgency.strip().lower() not in URGENCIES:
        raise ValueError(f"Invalid urgency: {urgency}")

    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer")

    return title.strip(), next(c for c in CATEGORIES if c.casefold() == category.strip().casefold()), urgency.strip().lower()

def validate_ticket_collection(tickets):
    """Reject a whole invalid collection before callers replace current state."""

    if not isinstance(tickets, list):
        raise ValueError("Ticket file must contain a list")

    seen_ids = set()
    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Every ticket must be an object")

        missing = TICKET_FIELDS - ticket.keys()

        if missing:
            raise ValueError(f"Ticket is missing required fields: {', '.join(sorted(missing))}")
        tid = ticket["id"]

        if (not isinstance(tid, str) or len(tid) < 4 or tid[0] != "T"
                or not tid[1:].isdigit() or int(tid[1:]) < 1):

            raise ValueError(f"Invalid ticket ID: {tid!r}")

        if tid in seen_ids:
            raise ValueError(f"Duplicate ticket ID: {tid}")

        seen_ids.add(tid)

        title, category, urgency = validate_ticket_fields(
            ticket["title"], ticket["category"], ticket["urgency"], ticket["affected_users"])
        if ticket["category"] != category:
            raise ValueError(f"Ticket {tid} has a non-canonical category")

        if ticket["urgency"] != urgency:
            raise ValueError(f"Ticket {tid} has a non-canonical urgency")

        from .tickets import calculate_priority

        if ticket["priority"] != calculate_priority(urgency, ticket["affected_users"]):
            raise ValueError(f"Ticket {tid} has inconsistent priority")

        if ticket["status"] not in STATUSES:
            raise ValueError(f"Ticket {tid} has invalid status")

        staff = ticket["assigned_to"]
        if staff is not None and (not isinstance(staff, str) or not staff.strip()):
            raise ValueError(f"Ticket {tid} has invalid assignment")

        notes = ticket["notes"]

        if not isinstance(notes, list):
            raise ValueError(f"Ticket {tid} notes must be a list")
        note_ids = set()

        for note in notes:
            if not isinstance(note, dict) or set(("note_id", "author", "message")) - note.keys():
                raise ValueError(f"Ticket {tid} has an invalid note")

            nid, author, message = note["note_id"], note["author"], note["message"]

            if (not isinstance(nid, str) or len(nid) < 2 or not nid.startswith("N")
                    or not nid[1:].isdigit() or int(nid[1:]) < 1):
                raise ValueError(f"Ticket {tid} has invalid note ID")

            if nid in note_ids:
                raise ValueError(f"Ticket {tid} has duplicate note ID {nid}")
            note_ids.add(nid)

            if not isinstance(author, str) or not author.strip():
                raise ValueError(f"Ticket {tid} has invalid note author")
                
            if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
                raise ValueError(f"Ticket {tid} has invalid note message")
    return True