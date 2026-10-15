"""
Search and filtering functions for CampusFlow.
All functions are read-only - they never modify tickets.
"""

from campusflownext.validation import (
    VALID_CATEGORIES,
    VALID_STATUSES,
    VALID_PRIORITIES
)


def search_tickets(tickets, title=None, category=None, status=None, priority=None):
    """
    Search tickets with optional filters.
   
    All supplied filters must match (AND logic).
    Empty/None filters mean "don't filter by this field".
   
    Args:
        tickets: list of tickets
        title: substring to search in title (case-insensitive)
        category: exact category match
        status: exact status match
        priority: exact priority match
   
    Returns:
        List of matching tickets (new list, original unchanged)
    """
    results = []
   
    for ticket in tickets:
        # Check title if provided
        if title and title.strip():
            if title.casefold() not in ticket["title"].casefold():
                continue
       
        # Check category if provided
        if category and category.strip():
            if category.casefold() != ticket["category"].casefold():
                continue
       
        # Check status if provided
        if status and status.strip():
            if status.casefold() != ticket["status"].casefold():
                continue
       
        # Check priority if provided
        if priority and priority.strip():
            if priority.casefold() != ticket["priority"].casefold():
                continue
       
        # All filters matched
        results.append(ticket)
   
    return results


def sort_by_priority(tickets):
    """
    Sort tickets by priority (critical > high > medium > low),
    then by numeric ticket ID for ties.
   
    Args:
        tickets: list of tickets
   
    Returns:
        New sorted list (original unchanged)
    """
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
   
    def sort_key(ticket):
        # Extract numeric part of ID (T001 → 1)
        ticket_num = int(ticket["id"][1:])
        return (priority_order[ticket["priority"]], ticket_num)
   
    return sorted(tickets, key=sort_key)


def get_work_queue(tickets):
    """
    Get OPEN tickets sorted by priority then ID.
    Only shows tickets with status "open".
   
    Args:
        tickets: list of tickets
   
    Returns:
        Sorted list of open tickets
    """
    open_tickets = [t for t in tickets if t["status"] == "open"]
    return sort_by_priority(open_tickets)


def validate_search_input(field, value):
    """
    Validate search filter input.
   
    Args:
        field: "category", "status", or "priority"
        value: the value to validate
   
    Returns:
        True if valid, False if invalid
    """
    if not value or not value.strip():
        return True  # Empty means "don't filter"
   
    valid_values = {
        "category": VALID_CATEGORIES,
        "status": VALID_STATUSES,
        "priority": VALID_PRIORITIES
    }
   
    if field not in valid_values:
        return False
   
    return value.casefold() in valid_values[field]