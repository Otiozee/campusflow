# CampusFlow

A command-line helpdesk ticket manager for Learn2Earn campus staff.

## Team Members
- Zedick - Ticket creation, validation, priority engine
- James - Assignment, workflow, queue, reports

## Setup
1. Clone the repo https://github.com/Otiozee/campusflow.git
2. change import paths to match the directory `campusflow`
3. Run `python3 main.py`

## Running the CLI

Menu options:
1. Create ticket - Add a new support ticket
2. List all tickets - Show all tickets
3. View ticket details - Show one ticket's full info
4. Assign ticket - Assign to staff member
5. Change status - Move through workflow
6. Show work queue - Open tickets by priority
7. Show reports - Statistics
8. Exit

## Testing
```bash
python -m unittest discover -s tests -v
```

### Priority Rules

- high urgency AND >= 10 users -> critical
- high urgency OR >= 10 users -> high
- medium urgency OR >= 3 users -> medium
- everything else -> low

### Status Workflow

- open -> in_progress (requires assignment) -> resolved
- resolved -> open (reopen)

### Data Storage

- Tickets saved to data/tickets.json
- Delete this file to start fresh

### Known Limitations

- No GUI (command-line only)
- No authentication
- Single-user at a time

### Pull Requests

PR #1: Ticket creation
PR #2: Workflow and reports

---

# CampusFlow Next

A reliable command-line helpdesk ticket manager for Learn2Earn campus staff.

## Team Members
- Zedick Otokpa (Engineer A) - Validation, notes, storage safety
- Solomon Emmanuel Aleke (Engineer B) - Search, reports, CLI understanding check

## Setup
1. Clone the repository https://github.com/otiozee/campusflow
2. change import paths to match the directory `campusflownext`
3. Run `python3 main.py`

## Running the CLI
```bash
python3 main.py
```
Menu options:
1. Create ticket - Add a new support ticket
2. List all tickets - Show all tickets
3. View ticket details - Show one ticket's full info
4. Assign ticket - Assign to staff member
5. Change status - Move through workflow
6. Show work queue - Open tickets by priority
7. Show reports - Statistics and analytics
8. Search tickets - Search with filters
9. Add follow-up note - Add note to open/in_progress ticket
10. View ticket notes - View all notes for a ticket
11. Engineering Understanding Check - 6-question quiz
12. Exit

## Testing
```bash
python -m unittest discover -s tests -v
```
### Priority Rules

- high urgency AND >= 10 users -> critical
- high urgency OR >= 10 users -> high
- medium urgency OR >= 3 users -> medium
- everything else -> low

### Status Workflow

- open -> in_progress (requires assignment) -> resolved
- resolved -> open (reopen)

### Notes Rules

- Notes can only be added to open or in_progress tickets
- Resolved tickets must be reopened before adding notes
- Note message must be 5-300 characters
- Notes are preserved through resolve and reopen

### Search

- Title search is case-insensitive (uses casefold)
- Optional filters: category, status, priority
- All supplied filters must match (AND logic)
- Empty filters mean "don't filter by that field"

### Data Storage

- Tickets saved to data/tickets.json
- Full validation on load (structure, IDs, business rules)
- Invalid files are rejected without changing current memory
- Delete data/tickets.json to start fresh

### Known Limitations

- No GUI (command-line only)
- No authentication
- Single-user at a time
- Search is substring-based (no fuzzy matching)

### Pull Requests

- PR #1: Validation and notes
- PR #2: Search and insights


