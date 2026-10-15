def get_report(tickets):
    """
    Generate comprehensive statistics about tickets.
   
    Args:
        tickets: list of tickets
   
    Returns:
        Dictionary with all report data
    """
    report = {
        "total": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        },
        "by_category": {
            "Network": 0,
            "Hardware": 0,
            "Software": 0,
            "Other": 0
        },
        "unresolved": 0,
        "resolved": 0,
        "resolution_percentage": 0.0
    }
   
    # Count tickets
    for ticket in tickets:
        # Status counts
        status = ticket["status"]
        if status in report["by_status"]:
            report["by_status"][status] += 1
       
        # Priority counts
        priority = ticket["priority"]
        if priority in report["by_priority"]:
            report["by_priority"][priority] += 1
       
        # Category counts
        category = ticket["category"]
        if category in report["by_category"]:
            report["by_category"][category] += 1
       
        # Resolved/unresolved
        if status == "resolved":
            report["resolved"] += 1
        else:
            report["unresolved"] += 1
   
    # Calculate resolution percentage
    if report["total"] > 0:
        report["resolution_percentage"] = (
            report["resolved"] / report["total"] * 100
        )
    else:
        report["resolution_percentage"] = 0.0
   
    return report


def get_work_queue(tickets):
    """
    Get OPEN tickets sorted by priority (critical > high > medium > low),
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