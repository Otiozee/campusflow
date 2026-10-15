"""
Central validation helpers for CampusFlow.
All validation functions raise ValueError with clear messages.
"""

VALID_CATEGORIES = ["network", "hardware", "software", "other"]
VALID_URGENCIES = ["low", "medium", "high"]
VALID_STATUSES = ["open", "in_progress", "resolved"]
VALID_PRIORITIES = ["critical", "high", "medium", "low"]


def validate_title(title):
    """Title must be non-blank after trimming."""
    if not title or not title.strip():
        raise ValueError("Title cannot be blank")
    return title.strip()


def validate_category(category):
    """Category must be one of the valid options."""
    if not category or category.lower() not in VALID_CATEGORIES:
        raise ValueError(
            f"Invalid category: {category}. Must be one of: "
            f"{', '.join(VALID_CATEGORIES)}"
        )
    return category.lower()


def validate_urgency(urgency):
    """Urgency must be low, medium, or high."""
    if not urgency or urgency.lower() not in VALID_URGENCIES:
        raise ValueError(
            f"Invalid urgency: {urgency}. Must be one of: "
            f"{', '.join(VALID_URGENCIES)}"
        )
    return urgency.lower()


def validate_affected_users(affected_users):
    """
    affected_users must be a strictly positive integer.
    Rejects floats, strings, and booleans.
    """
    # Reject booleans (bool is subclass of int in Python)
    if isinstance(affected_users, bool):
        raise ValueError("Affected users must be a positive integer, not a boolean")
    
    # Reject non-integers
    if not isinstance(affected_users, int):
        raise ValueError("Affected users must be a positive integer")
    
    # Reject non-positive
    if affected_users <= 0:
        raise ValueError("Affected users must be a positive integer")
    
    return affected_users


def validate_status(status):
    """Status must be one of the valid options."""
    if not status or status.lower() not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status: {status}. Must be one of: "
            f"{', '.join(VALID_STATUSES)}"
        )
    return status.lower()


def validate_priority(priority):
    """Priority must be one of the valid options."""
    if not priority or priority.lower() not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority: {priority}. Must be one of: "
            f"{', '.join(VALID_PRIORITIES)}"
        )
    return priority.lower()


def validate_staff_name(staff_name):
    """Staff name must be non-blank."""
    if not staff_name or not staff_name.strip():
        raise ValueError("Staff name cannot be blank")
    return staff_name.strip()


def validate_note_author(author):
    """Note author must be non-blank."""
    if not author or not author.strip():
        raise ValueError("Note author cannot be blank")
    return author.strip()


def validate_note_message(message):
    """Note message must be 5-300 characters after trimming."""
    if not message:
        raise ValueError("Note message cannot be blank")
    
    trimmed = message.strip()
    if len(trimmed) < 5:
        raise ValueError("Note message must be at least 5 characters")
    if len(trimmed) > 300:
        raise ValueError("Note message cannot exceed 300 characters")
    
    return trimmed


def validate_ticket_id(ticket_id):
    """Ticket ID must be a string in format T001, T002, etc."""
    if not ticket_id or not isinstance(ticket_id, str):
        raise ValueError("Ticket ID must be a string")
    
    if not ticket_id.startswith("T") or not ticket_id[1:].isdigit():
        raise ValueError(f"Invalid ticket ID format: {ticket_id}")
    
    return ticket_id


def validate_ticket(ticket):
    """
    Validate a complete ticket dictionary.
    Returns the validated ticket if valid.
    Raises ValueError if any field is invalid.
    """
    # Check required keys exist
    required_keys = [
        "id", "title", "category", "urgency", "affected_users",
        "priority", "status", "assigned_to", "notes"
    ]
    for key in required_keys:
        if key not in ticket:
            raise ValueError(f"Ticket missing required field: {key}")
    
    # Validate each field
    validate_ticket_id(ticket["id"])
    validate_title(ticket["title"])
    validate_category(ticket["category"])
    validate_urgency(ticket["urgency"])
    validate_affected_users(ticket["affected_users"])
    validate_priority(ticket["priority"])
    validate_status(ticket["status"])
    
    # assigned_to can be None or non-blank string
    if ticket["assigned_to"] is not None:
        validate_staff_name(ticket["assigned_to"])
    
    # Validate notes structure
    if not isinstance(ticket["notes"], list):
        raise ValueError("Notes must be a list")
    
    for note in ticket["notes"]:
        validate_note(note)
    
    return ticket


def validate_note(note):
    """Validate a single note dictionary."""
    required_keys = ["note_id", "author", "message"]
    for key in required_keys:
        if key not in note:
            raise ValueError(f"Note missing required field: {key}")
    
    if not isinstance(note["note_id"], str) or not note["note_id"].startswith("N"):
        raise ValueError(f"Invalid note ID: {note['note_id']}")
    
    validate_note_author(note["author"])
    validate_note_message(note["message"])
    
    return note


def can_transition(current_status, new_status, assigned_to):
    """
    Check if a status transition is valid.
    
    Valid transitions:
    - open → in_progress (requires assignment)
    - open → resolved
    - in_progress → resolved
    - resolved → open (reopen)
    
    Returns:
        True if valid, raises ValueError if invalid
    """
    current = validate_status(current_status)
    new = validate_status(new_status)
    
    valid_transitions = {
        "open": ["in_progress", "resolved"],
        "in_progress": ["resolved"],
        "resolved": ["open"]
    }
    
    if new not in valid_transitions.get(current, []):
        raise ValueError(
            f"Cannot move ticket from '{current}' to '{new}'"
        )
    
    # Special rule: can't go to in_progress without assignment
    if new == "in_progress" and assigned_to is None:
        raise ValueError("Cannot start work on unassigned ticket")
    
    return True
