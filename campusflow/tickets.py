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


def create_ticket(tickets, title, category, urgency, affected_users, ):
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
    # Validation
    if not title or not title.strip():
        raise ValueError("Title cannot be blank")
    
    if category.lower() not in ["network", "hardware", "software", "other"]:
        raise ValueError(f"Invalid category: {category}")
    
    if urgency.lower() not in ["low", "medium", "high"]:
        raise ValueError(f"Invalid urgency: {urgency}")
    
    if not isinstance(affected_users, int) or isinstance(affected_users, bool) or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer")
    
    # Generate ID
    next_num = len(tickets) + 1
    ticket_id = f"T{next_num:03d}"
    
    # Calculate priority
    priority = calculate_priority(urgency, affected_users)
    
    # Create ticket
    ticket = {
        "id": ticket_id,
        "title": title.strip(),
        "category": category.capitalize(),
        "urgency": urgency.lower(),
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
        "notes":[]
    }
    
    tickets.append(ticket)
    return ticket
