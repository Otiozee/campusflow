# Baseline Check

## Repository and commit
terseer333/CampusFlowNext, main at b0a9948
("feat: add CLI menu and update README")

## Run command
python3 -m unittest discover -s tests -v

## Result
Ran 24 tests. OK (all passing), before any new changes.

## Three manual inputs (run with python3 main.py)
1. Input: Create ticket. Title "system crash", category "hardware", urgency "high", affected users 8.
   Expected: created with priority "high" (rule 2: high urgency, fewer than 10 users).
   Actual: "✓ Created T001 with high priority". Matches.

2. Input: List all tickets (option 2).
   Expected: T001 shown as open.
   Actual: "T001: system crash [high] (open)". Matches.

3. Input: Assign ticket T001 to "kingsley" (option 4).
   Expected: T001 assigned, status still open.
   Actual: "✓ Assigned T001 to kingsley". Matches.

## Observations (not yet tested)
- The menu has 8 options: no notes, search, or understanding check.
- The last menu prompt was left blank (Enter with no choice). Its behaviour was not recorded.
- Option 3 (view) was run before assignment, so it showed "Assigned To: Unassigned".
