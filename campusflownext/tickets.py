from campusflownext.validation import (
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    validate_ticket,
    can_transition
)


def calculate_priority(urgency, affected_users):
    """
    Calculate ticket priority using the 4-rule cascade.
    
    Args:
        urgency: "low", "medium", or "high"
        affected_users: positive integer
    
    Returns:
        "critical", "high", "medium", or "low"
    """
    urgency = urgency.lower()
    
    # RULE 1: high urgency AND >= 10 users
    if urgency == "high" and affected_users >= 10:
        return "critical"
    
    # RULE 2: high urgency OR >= 10 users
    if urgency == "high" or affected_users >= 10:
        return "high"
    
    # RULE 3: medium urgency OR >= 3 users
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    
    # RULE 4: everything else
    return "low"


def create_ticket(tickets, title, category, urgency, affected_users):
    """
    Create and validate a new ticket.
    
    Args:
        tickets: list of existing tickets
        title: string, cannot be blank
        category: "Network", "Hardware", "Software", "Other"
        urgency: "low", "medium", "high"
        affected_users: positive integer
    
    Returns:
        New ticket dictionary
    
    Raises:
        ValueError: if inputs are invalid
    """
    # Validate all inputs BEFORE creating ticket
    valid_title = validate_title(title)
    valid_category = validate_category(category)
    valid_urgency = validate_urgency(urgency)
    valid_users = validate_affected_users(affected_users)
    
    # Generate ID
    next_num = len(tickets) + 1
    ticket_id = f"T{next_num:03d}"
    
    # Calculate priority
    priority = calculate_priority(valid_urgency, valid_users)
    
    # Create ticket
    ticket = {
        "id": ticket_id,
        "title": valid_title,
        "category": valid_category.capitalize(),
        "urgency": valid_urgency,
        "affected_users": valid_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
        "notes": []
    }
    
    tickets.append(ticket)
    return ticket


def find_ticket(tickets, ticket_id):
    """Helper function to find a ticket by ID."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    return None
