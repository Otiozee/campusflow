# AI Learning Log

## Fellow: Zedick

### Interaction #1 — JSON Persistence

**Problem:** I don't understand how to save Python dictionaries to a file

**My initial understanding:** JSON is a text format, but I'm not sure how to convert Python data back and forth

**Prompt to AI:** "Explain json.dump() and json.load() with a 5-line example using a simple shopping list. Then quiz me on what happens if the file doesn't exist."

**Useful AI guidance:** 
- dump() writes Python data to file
- load() reads file back into Python
- Need to handle FileNotFoundError

**My experiment:**
```python
import json

# Test saving
data = {"items": ["apple", "bread"], "total": 5.50}
with open("test.json", "w") as f:
    json.dump(data, f)

# Test loading
with open("test.json", "r") as f:
    loaded = json.load(f)
    
print(loaded["total"])  # I predicted: 5.5 ✓
```
Verification: Ran code, checked test.json content, it worked!
Decision: ACCEPTED — I'll use this pattern for tickets.json
Related file: campusflow/storage.py
What I can now explain: json.dump() takes Python data and a file, converts to text and saves it. json.load() reverses this.

### Interaction 2 — bool is subclass of int
Problem: My test for rejecting decimal affected_users was failing
My initial understanding: isinstance(5.5, int) should be False
Prompt to AI: "My test test_reject_decimal_affected_users is failing. Here's my code and traceback. What's wrong?"
Useful AI guidance:

Python's bool is a subclass of int
isinstance(True, int) returns True
Need to check for bool explicitly

My experiment:
print(isinstance(5.5, int))  # False ✓
print(isinstance(True, int))  # True - this is the problem!

Verification: Added or isinstance(affected_users, bool) to validation
Decision: IMPROVED AI suggestion - added bool check to validation
Related file: campusflow/tickets.py
What I can now explain: In Python, bool is a subclass of int, so True == 1 and isinstance(True, int) is True.

### Interaction 3 — unittest assertRaises
Problem: I wasn't sure how to test that functions raise errors
My initial understanding: I thought I needed try/except in tests
Prompt to AI: "How do I test that a function raises ValueError in Python unittest?"
Useful AI guidance:

Use assertRaises context manager
Can check error message with str(context.exception)

My experiment:
import unittest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class TestDivide(unittest.TestCase):
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertIn("Cannot divide", str(context.exception))

# This passed!
Verification: Ran the test, it passed
Decision: ACCEPTED — using assertRaises in all my tests
Related file: tests/test_tickets.py
What I can now explain: assertRaises checks that an exception is raised, and I can inspect the error message.

---

# AI Learning Log

## Fellow: James

### Interaction #1 — Exception Handling

**Problem:** I wasn't sure how to handle errors gracefully in Python

**My initial understanding:** I thought errors would crash the program

**Prompt to AI:** "Explain try/except/else/finally with a 5-line example. I want to understand when each block runs."

**Useful AI guidance:** 
- try: code that might fail
- except: runs if error occurs
- else: runs if no error
- finally: always runs

**My experiment:**
```python
try:
    num = int("abc")  # This will fail
except ValueError:
    print("That's not a number!")
else:
    print("Valid number:", num)
finally:
    print("This always runs")
```

# Output: "That's not a number!" then "This always runs"

Verification: Ran it, got expected output
Decision: ACCEPTED — using try/except in CLI
Related file: main.py
What I can now explain: try/except catches errors so the program doesn't crash.

### Interaction #2 — Git Merge Conflicts
Problem: I was worried about merge conflicts when merging branches
My initial understanding: Merge conflicts mean I broke something
Prompt to AI: "What causes merge conflicts and how do I resolve them?"
Useful AI guidance:

Conflicts happen when both branches change same lines
Look for <<<<<<< ======= >>>>>>> markers
Choose correct version, remove markers

My experiment:
# Created two branches, changed same line in both
# Got conflict markers:
<<<<<<< HEAD
print("Hello from main")
=======
print("Hello from feature")
>>>>>>> feature

# Resolved by keeping: print("Hello from feature")

Verification: Resolved conflict, code worked
Decision: ACCEPTED — not scared of conflicts anymore
Related file: Git workflow
What I can now explain: Conflicts are normal, just read markers and choose correct code.

### Interaction #3 — List Sorting with Keys
Problem: I needed to sort tickets by priority then ID
My initial understanding: I thought sorted() only worked on simple lists
Prompt to AI: "How do I sort a list of dictionaries by two keys in Python?"
Useful AI guidance:

Use key parameter with a function
Return a tuple for multiple sort criteria

My experiment:
```
tickets = [
    {"id": "T002", "priority": "high"},
    {"id": "T001", "priority": "critical"},
    {"id": "T003", "priority": "high"}
]
```

priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def sort_key(t):
    return (priority_order[t["priority"]], int(t["id"][1:]))

sorted_tickets = sorted(tickets, key=sort_key)
# Result: T001 (critical), T002 (high), T003 (high)

Verification: Ran it, got correct order
Decision: ACCEPTED — using this for work queue
Related file: campusflow/reports.py
What I can now explain: sorted() with key function can sort by multiple criteria using tuples.

---

## Fellow: Zedick Otokpa

### Interaction #1 — Validate Before Mutate

**Problem:** I need to validate a dictionary BEFORE changing it, so failed operations don't corrupt data

**My initial understanding:** I thought checking inputs one by one was enough

**Prompt to AI:** "Explain how to validate a dictionary BEFORE mutating it, using a book library example, then quiz me."

**Useful AI guidance:** 
- Validate ALL inputs first, collect errors
- Only mutate if everything passes
- Use a copy for validation if needed

**My experiment:**
```python
# Before (bad - mutates then validates)
def add_book_bad(library, book):
    library.append(book)  # Mutates first!
    if not book.get("title"):
        library.pop()  # Too late, already changed

# After (good - validates first)
def add_book_good(library, book):
    if not book.get("title"):
        raise ValueError("Title required")
    if not book.get("author"):
        raise ValueError("Author required")
    library.append(book)  # Only mutate if valid
```

Verification: Ran both, confirmed good version doesn't change list on error
Decision: ACCEPTED — validate everything before any mutation
Related file: campusflow/validation.py
What I can now explain: Validate all inputs first, only mutate if everything passes.

### Interaction #2 — JSON Validation After Decoding
Problem: json.load() succeeds but returns unsafe data
My initial understanding: I thought if json.load() works, the data is fine
Prompt to AI: "Why might json.load succeed but return unsafe or inconsistent business data?"
Useful AI guidance:

JSON just checks syntax, not business rules
Could have duplicate IDs, missing fields, wrong types
Need to validate structure AFTER decoding

My experiment:
```
import json

# This JSON is syntactically valid but business-invalid
bad_data = '''
[
    {"id": "T001", "title": "First"},
    {"id": "T001", "title": "Duplicate!"}
]
'''

tickets = json.loads(bad_data)  # This succeeds!
# But we have duplicate IDs - business rule violation

# Need to validate after loading
ids = [t["id"] for t in tickets]
if len(ids) != len(set(ids)):
    raise ValueError("Duplicate ticket IDs found")
```

Verification: Ran it, confirmed json.load succeeds but data is invalid
Decision: ACCEPTED - always validate business rules after JSON decode
Related file: campusflow/storage.py
What I can now explain: JSON validation is separate from JSON parsing.

---

