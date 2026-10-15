import copy


def search_titles(tickets, text):
    needle = text.strip().casefold()          # "  WI-FI " -> "wi-fi"
    results = []
    for ticket in tickets:
        if needle in ticket["title"].casefold():   # "" matches everything
            results.append(copy.deepcopy(ticket))  # copy so the stored ticket can't be changed
    return results

def search_filtered(tickets, text="", category="", status="", priority=""):
    results = search_titles(tickets, text)                       # title step (already copies)
    if category:
        results = [t for t in results if t["category"] == category]
    if status:
        results = [t for t in results if t["status"] == status]
    if priority:
        results = [t for t in results if t["priority"] == priority]
    return results