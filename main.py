import sys
from campusflownext.tickets import create_ticket, find_ticket
from campusflownext.workflow import assign_ticket, change_status
from campusflownext.reports import get_report, get_work_queue
from campusflownext.storage import load_tickets, save_tickets
from campusflownext.notes import add_note, get_notes
from campusflownext.search import search_tickets, validate_search_input
from campusflownext.understanding_check import (
    QUESTION_BANK,
    calculate_score,
    validate_answer,
    get_question_text,
    get_correct_answer,
    get_explanation
)


def display_menu():
    print("\n" + "="*50)
    print("CAMPUSFLOW NEXT - Helpdesk Ticket Manager")
    print("="*50)
    print("1. Create ticket")
    print("2. List all tickets")
    print("3. View ticket details")
    print("4. Assign ticket")
    print("5. Change status")
    print("6. Show work queue")
    print("7. Show reports")
    print("8. Search tickets")
    print("9. Add follow-up note")
    print("10. View ticket notes")
    print("11. Engineering Understanding Check")
    print("12. Exit")
    print("="*50)


def list_tickets(tickets):
    if not tickets:
        print("No tickets found.")
        return
    for t in tickets:
        print(f"{t['id']}: {t['title']} [{t['priority']}] ({t['status']})")


def view_ticket(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        print(f"Ticket {ticket_id} not found.")
        return
    
    print(f"\nID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected Users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned To: {ticket['assigned_to'] or 'Unassigned'}")
    print(f"Notes: {len(ticket['notes'])}")


def search_menu(tickets):
    """Search tickets with optional filters."""
    print("\n--- SEARCH TICKETS ---")
    print("(Press Enter to skip any filter)")
    
    title = input("Title contains: ").strip()
    
    # Category filter
    while True:
        category = input("Category (Network/Hardware/Software/Other): ").strip()
        if validate_search_input("category", category):
            break
        print("Invalid category. Try again.")
    
    # Status filter
    while True:
        status = input("Status (open/in_progress/resolved): ").strip()
        if validate_search_input("status", status):
            break
        print("Invalid status. Try again.")
    
    # Priority filter
    while True:
        priority = input("Priority (critical/high/medium/low): ").strip()
        if validate_search_input("priority", priority):
            break
        print("Invalid priority. Try again.")
    
    results = search_tickets(
        tickets,
        title=title or None,
        category=category or None,
        status=status or None,
        priority=priority or None
    )
    
    if not results:
        print("\nNo tickets match your search.")
        return
    
    print(f"\nFound {len(results)} matching ticket(s):")
    for t in results:
        print(f"  {t['id']}: {t['title']} [{t['priority']}] ({t['status']}) "
              f"Assigned: {t['assigned_to'] or 'Unassigned'}")


def add_note_menu(tickets):
    """Add a follow-up note to a ticket."""
    print("\n--- ADD FOLLOW-UP NOTE ---")
    
    ticket_id = input("Ticket ID: ").strip()
    author = input("Your name: ").strip()
    message = input("Note message (5-300 chars): ").strip()
    
    try:
        note = add_note(tickets, ticket_id, author, message)
        save_tickets(tickets)
        print(f"✓ Note {note['note_id']} added to {ticket_id}")
    except ValueError as e:
        print(f"✗ Error: {e}")


def view_notes_menu(tickets):
    """View all notes for a ticket."""
    print("\n--- VIEW TICKET NOTES ---")
    
    ticket_id = input("Ticket ID: ").strip()
    
    try:
        notes = get_notes(tickets, ticket_id)
        if not notes:
            print(f"No notes for ticket {ticket_id}.")
            return
        
        print(f"\nNotes for {ticket_id}:")
        for note in notes:
            print(f"  {note['note_id']} | {note['author']}: {note['message']}")
    except ValueError as e:
        print(f"✗ Error: {e}")


def understanding_check():
    """Run the Engineering Understanding Check quiz."""
    print("\n--- ENGINEERING UNDERSTANDING CHECK ---")
    print("Answer each question with A, B, C, or D.")
    print("You'll be asked to explain 2 answers at the end.\n")
    
    answers = []
    explanations = {}
    
    for i in range(len(QUESTION_BANK)):
        print(get_question_text(i))
        
        # Get valid answer
        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            if validate_answer(answer):
                break
            print("Invalid answer. Please enter A, B, C, or D.")
        
        answers.append(answer)
        
        # Show feedback
        correct = get_correct_answer(i)
        if answer == correct:
            print("✓ Correct!\n")
        else:
            print(f"✗ Incorrect. The correct answer is {correct}.\n")
    
    # Ask for explanations on 2 answers
    print("\n--- EXPLANATIONS ---")
    print("Please explain why you chose your answers for questions 1 and 3:")
    
    for q_num in [0, 2]:  # Questions 1 and 3 (0-indexed)
        print(f"\nQuestion {q_num + 1}: {QUESTION_BANK[q_num]['question']}")
        print(f"Your answer: {answers[q_num]}")
        explanation = input("Why did you choose this answer? ").strip()
        explanations[q_num] = explanation
    
    # Calculate score
    score = calculate_score(answers)
    
    print("\n" + "="*50)
    print(f"YOUR SCORE: {score}/6")
    print("="*50)
    
    # Show explanations for review
    print("\n--- EXPLANATION REVIEW ---")
    for q_num in [0, 2]:
        print(f"\nQ{q_num + 1}: {QUESTION_BANK[q_num]['explanation']}")
        print(f"Your explanation: {explanations.get(q_num, 'No explanation provided')}")
    
    return score


def main():
    tickets = load_tickets()
    
    while True:
        display_menu()
        choice = input("Enter choice (1-12): ").strip()
        
        try:
            if choice == "1":
                title = input("Title: ").strip()
                category = input("Category (Network/Hardware/Software/Other): ").strip()
                urgency = input("Urgency (low/medium/high): ").strip()
                users = int(input("Affected users: ").strip())
                
                ticket = create_ticket(tickets, title, category, urgency, users)
                save_tickets(tickets)
                print(f"✓ Created {ticket['id']} with {ticket['priority']} priority")
            
            elif choice == "2":
                list_tickets(tickets)
            
            elif choice == "3":
                view_ticket(tickets)
            
            elif choice == "4":
                ticket_id = input("Ticket ID: ").strip()
                staff = input("Staff name: ").strip()
                assign_ticket(tickets, ticket_id, staff)
                save_tickets(tickets)
                print(f"✓ Assigned {ticket_id} to {staff}")
            
            elif choice == "5":
                ticket_id = input("Ticket ID: ").strip()
                new_status = input("New status (open/in_progress/resolved): ").strip()
                change_status(tickets, ticket_id, new_status)
                save_tickets(tickets)
                print(f"✓ {ticket_id} is now {new_status}")
            
            elif choice == "6":
                queue = get_work_queue(tickets)
                if not queue:
                    print("No open tickets in queue.")
                else:
                    print("\nWORK QUEUE (by priority):")
                    for t in queue:
                        print(f"  {t['id']}: {t['title']} [{t['priority']}]")
            
            elif choice == "7":
                report = get_report(tickets)
                print(f"\nTotal tickets: {report['total']}")
                print("\nBy Status:")
                for status, count in report["by_status"].items():
                    print(f"  {status}: {count}")
                print("\nBy Priority:")
                for priority, count in report["by_priority"].items():
                    print(f"  {priority}: {count}")
                print("\nBy Category:")
                for category, count in report["by_category"].items():
                    print(f"  {category}: {count}")
                print(f"\nUnresolved: {report['unresolved']}")
                print(f"Resolved: {report['resolved']}")
                print(f"Resolution Rate: {report['resolution_percentage']:.1f}%")
            
            elif choice == "8":
                search_menu(tickets)
            
            elif choice == "9":
                add_note_menu(tickets)
            
            elif choice == "10":
                view_notes_menu(tickets)
            
            elif choice == "11":
                understanding_check()
            
            elif choice == "12":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter 1-12.")
        
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
    main()
