def find_ticket(tickets, ticket_id):

    for ticket in tickets:
        if ticket["id"] == ticket_id:

            return ticket
    return None

def assign_ticket(tickets, ticket_id, staff_name):

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be blank")

    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} not found")
    if ticket["status"] == "resolved":
        raise ValueError("Cannot change assignment on a resolved ticket; reopen it first")
    ticket["assigned_to"] = staff_name.strip()
    return ticket

def change_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} not found")

    if not isinstance(new_status, str):
        raise ValueError("Invalid status")

    new = new_status.strip().lower()

    if new not in ("open", "in_progress", "resolved"):
        raise ValueError(f"Invalid status: {new_status}")

    current = ticket["status"]

    valid_transitions = {
        "open": ["in_progress"],
        "in_progress": ["resolved"],
        "resolved": ["open"]
    }

    if new not in valid_transitions.get(current, []):
        raise ValueError(f"Cannot move ticket from '{current}' to '{new}'")

    if new == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Cannot start work on unassigned ticket")

    ticket["status"] = new
    return ticket
