import sys
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status
from campusflow.reports import get_work_queue, get_report
from campusflow.storage import load_tickets, save_tickets

def display_menu():
    print("\n" + "="*50)
    print("CAMPUSFLOW - Helpdesk Ticket Manager")
    print("="*50)
    print("1. Create ticket")
    print("2. List all tickets")
    print("3. View ticket details")
    print("4. Assign ticket")
    print("5. Change status")
    print("6. Show work queue")
    print("7. Show reports")
    print("8. Exit")
    print("="*50)

def list_tickets(tickets):
    if not tickets:
        print("No tickets found.")
        return
    for t in tickets:
        print(f"{t['id']}: {t['title']} [{t['priority']}] ({t['status']})")

def view_ticket(tickets):
    ticket_id = input("Enter ticket ID: ").strip().upper()
    for t in tickets:
        if t["id"] == ticket_id:
            print(f"\nID: {t['id']}")
            print(f"Title: {t['title']}")
            print(f"Category: {t['category']}")
            print(f"Urgency: {t['urgency']}")
            print(f"Affected Users: {t['affected_users']}")
            print(f"Priority: {t['priority']}")
            print(f"Status: {t['status']}")
            print(f"Assigned To: {t['assigned_to'] or 'Unassigned'}")
            return
    print(f"Ticket {ticket_id} not found.")

def main():
    tickets = load_tickets()
    
    while True:
        display_menu()
        choice = input("Enter choice (1-8): ").strip()
        
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
                ticket_id = input("Ticket ID: ").strip().upper()
                staff = input("Staff name: ").strip()
                assign_ticket(tickets, ticket_id, staff)
                save_tickets(tickets)
                print(f"✓ Assigned {ticket_id} to {staff}")
            
            elif choice == "5":
                ticket_id = input("Ticket ID: ").strip().upper()
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
            
            elif choice == "8":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter 1-8.")
        
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
    main()
