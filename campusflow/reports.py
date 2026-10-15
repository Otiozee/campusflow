def get_work_queue(tickets):
    """
    Get open tickets sorted by priority (critical > high > medium > low),
    then by numeric ticket ID.
        
    Args:
        tickets: list of tickets
    
    Returns:
        Sorted list of open tickets
    """
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

    open_tickets = [t for t in tickets if t["status"] == "open"]

    def sort_key(ticket):
     # Extract numeric part of ID (T001 → 1)
        ticket_num = int(ticket["id"][1:])
        return (priority_order[ticket["priority"]], ticket_num)

    return sorted(open_tickets, key=sort_key)


def get_report(tickets):
    """
    Generate statistics about tickets.

    Returns a dictionary with:
        total, by_status, by_priority, by_category,
        unresolved, resolved, resolution_percent
    """
    report = {
        "total": len(tickets),
        "by_status": {"open": 0, "in_progress": 0, "resolved": 0},
        "by_priority": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        "by_category": {"Network": 0, "Hardware": 0, "Software": 0, "Other": 0},
    }

    for ticket in tickets:
        report["by_status"][ticket["status"]] += 1
        report["by_priority"][ticket["priority"]] += 1
        report["by_category"][ticket["category"]] += 1

    resolved = report["by_status"]["resolved"]
    report["resolved"] = resolved
    report["unresolved"] = report["by_status"]["open"] + report["by_status"]["in_progress"]

    # Empty list: 0% instead of dividing by zero.
    if report["total"] == 0:
        report["resolution_percent"] = 0.0
    else:
        report["resolution_percent"] = resolved / report["total"] * 100

    return report
