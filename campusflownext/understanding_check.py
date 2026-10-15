"""
Engineering Understanding Check - interactive quiz.
Question bank is separate from scoring logic.
"""

# Question bank - separate from scoring logic
QUESTION_BANK = [
    {
        "question": (
            "Q1. Ticket T001 is open and unassigned. "
            "A user tries to move it to in_progress."
        ),
        "options": [
            "A. Accept",
            "B. Reject and preserve all data",
            "C. Resolve it automatically",
            "D. Remove ticket"
        ],
        "correct": "B",
        "explanation": (
            "An unassigned ticket cannot move to in_progress. "
            "The system must reject this and keep all data unchanged."
        )
    },
    {
        "question": (
            "Q2. The app has zero tickets. "
            "What should resolution percentage display?"
        ),
        "options": [
            "A. Crash",
            "B. 100%",
            "C. 0%",
            "D. Divide by one without explanation"
        ],
        "correct": "C",
        "explanation": (
            "With zero tickets, resolution percentage should be 0% "
            "without causing a division error."
        )
    },
    {
        "question": (
            "Q3. Filter title='wifi', category='Network', status='open'. "
            "Which records should match?"
        ),
        "options": [
            "A. Any record matching one filter",
            "B. Only records matching all supplied filters",
            "C. All network records",
            "D. All open records"
        ],
        "correct": "B",
        "explanation": (
            "Combined filters use AND logic - ALL supplied filters "
            "must match for a ticket to be included."
        )
    },
    {
        "question": (
            "Q4. A resolved ticket receives 'Add note'. "
            "What should happen?"
        ),
        "options": [
            "A. Append anyway",
            "B. Delete old notes",
            "C. Reject until reopened",
            "D. Change status silently"
        ],
        "correct": "C",
        "explanation": (
            "Resolved tickets cannot accept new notes. "
            "The ticket must be reopened first."
        )
    },
    {
        "question": (
            "Q5. The JSON file includes two tickets with the same ID. "
            "What should load do?"
        ),
        "options": [
            "A. Keep both",
            "B. Replace memory with duplicates",
            "C. Reject the load without changing current memory",
            "D. Rename IDs silently"
        ],
        "correct": "C",
        "explanation": (
            "Duplicate IDs violate data integrity. "
            "The load must be rejected and current memory preserved."
        )
    },
    {
        "question": (
            "Q6. A PR changes validation but has no negative-case tests. "
            "Best review action?"
        ),
        "options": [
            "A. Approve because it runs",
            "B. Request focused tests and reasoning",
            "C. Merge immediately",
            "D. Ask AI to approve it"
        ],
        "correct": "B",
        "explanation": (
            "Changes to validation need negative tests to prove "
            "invalid inputs are rejected correctly."
        )
    }
]


def calculate_score(answers):
    """
    Calculate quiz score based on answers.
   
    Args:
        answers: list of answers (A, B, C, or D)
   
    Returns:
        Score (0-6)
    """
    score = 0
    for i, answer in enumerate(answers):
        if i < len(QUESTION_BANK) and answer == QUESTION_BANK[i]["correct"]:
            score += 1
    return score


def validate_answer(answer):
    """
    Validate that answer is A, B, C, or D.
   
    Args:
        answer: user input
   
    Returns:
        True if valid, False if invalid
    """
    return answer and answer.strip().upper() in ["A", "B", "C", "D"]


def get_question_text(index):
    """
    Get question text for a given index.
   
    Args:
        index: question index (0-5)
   
    Returns:
        Question text string
    """
    if 0 <= index < len(QUESTION_BANK):
        q = QUESTION_BANK[index]
        text = q["question"] + "\n"
        for option in q["options"]:
            text += "  " + option + "\n"
        return text
    return "Invalid question index"


def get_correct_answer(index):
    """
    Get correct answer for a given index.
   
    Args:
        index: question index (0-5)
   
    Returns:
        Correct answer letter
    """
    if 0 <= index < len(QUESTION_BANK):
        return QUESTION_BANK[index]["correct"]
    return None


def get_explanation(index):
    """
    Get explanation for a given index.
   
    Args:
        index: question index (0-5)
   
    Returns:
        Explanation string
    """
    if 0 <= index < len(QUESTION_BANK):
        return QUESTION_BANK[index]["explanation"]
    return "No explanation available"