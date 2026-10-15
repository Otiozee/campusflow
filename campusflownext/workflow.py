from campusflownext.validation import (
    validate_staff_name,
    validate_ticket_id,
    validate_status,
    can_transition
)
from campusflownext.tickets import find_ticket


def assign_ticket(tickets, ticket_id, staff_name):
    """
    Assign a ticket to a staff member.
    
    Args:
        tickets: list of tickets
        ticket_id: string like "T001"
        staff_name: non-empty string
    
    Returns:
        Updated ticket
    
    Raises:
        ValueError: if ticket not found, staff_name blank, or ticket resolved
    """
    # Validate inputs first
    valid_ticket_id = validate_ticket_id(ticket_id)
    valid_staff = validate_staff_name(staff_name)
    
    # Find ticket
    ticket = find_ticket(tickets, valid_ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket {valid_ticket_id} not found")
    
    # Cannot assign resolved ticket
    if ticket["status"] == "resolved":
        raise ValueError(
            f"Cannot assign resolved ticket {valid_ticket_id}. "
            "Reopen the ticket first."
        )
    
    # Mutate only after all validation passes
    ticket["assigned_to"] = valid_staff
    return ticket


def change_status(tickets, ticket_id, new_status):
    """
    Change ticket status following workflow rules.
    
    Valid transitions:
    - open → in_progress (requires assigned_to)
    - open → resolved
    - in_progress → resolved
    - resolved → open (reopen)
    
    Args:
        tickets: list of tickets
        ticket_id: string like "T001"
        new_status: "open", "in_progress", or "resolved"
    
    Returns:
        Updated ticket
    
    Raises:
        ValueError: if invalid transition
    """
    # Validate inputs first
    valid_ticket_id = validate_ticket_id(ticket_id)
    valid_new_status = validate_status(new_status)
    
    # Find ticket
    ticket = find_ticket(tickets, valid_ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket {valid_ticket_id} not found")
    
    # Check if transition is valid
    can_transition(ticket["status"], valid_new_status, ticket["assigned_to"])
    
    # Mutate only after validation passes
    ticket["status"] = valid_new_status
    return ticket
