import copy


def search_titles(tickets, text):
    needle = text.strip().casefold()          # "  WI-FI " -> "wi-fi"
    results = []
    for ticket in tickets:
        if needle in ticket["title"].casefold():   # "" matches everything
            results.append(copy.deepcopy(ticket))  # copy so the stored ticket can't be changed
    return results