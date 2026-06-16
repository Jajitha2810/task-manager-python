from manager import TaskManager
from display import DisplayManager
from task import Priority, Status

class TaskManagerApp:
    """
    Main CLI Application for Task Manager
    
    Author: Jajitha
    Course: Python Project Development
    """
    
    def __init__(self):
        self.manager = TaskManager()
        self.display = DisplayManager()
    
    def get_priority(self):
        """Get priority input from user"""
        print("\nSelect Priority:")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        choice = input("Enter choice (1-3): ").strip()
        priority_map = {
            '1': Priority.HIGH,
            '2': Priority.MEDIUM,
            '3': Priority.LOW
        }
        return priority_map.get(choice, Priority.MEDIUM)
    
    def get_deadline(self):
        """Get deadline input from user"""
        deadline_input = input(
            "Enter deadline (YYYY-MM-DD) or press Enter to skip: "
        ).strip()
        
        if deadline_input:
            try:
                deadline = datetime.strptime(
                    deadline_input,
                    '%Y-%m-%d'
                )
                return deadline.isoformat()
            except ValueError:
                self.display.print_error(
                    "Invalid date format! Skipping deadline."
                )
        return None
    
    def add_task(self):
        """Handle add task flow"""
        print(f"\n{'-'*30}")
        print("ADD NEW TASK")
        print(f"{'-'*30}")
        
        title = input("Task title: ").strip()
        if not title:
            self.display.print_error("Title cannot be empty!")
            return
        
        description = input(
            "Description (optional): "
        ).strip()
        priority = self.get_priority()
        category = input(
            "Category (default: General): "
        ).strip() or "General"
        deadline = self.get_deadline()
        
        self.manager.add_task(
            title=title,
            description=description,
            priority=priority,
            category=category,
            deadline=deadline
        )
        self.display.print_success(
            f"Task '{title}' added successfully!"
        )
    
    def view_all_tasks(self):
        """Display all tasks"""
        tasks = self.manager.get_all_tasks()
        self.display.print_task_list(tasks)
    
    def update_task(self):
        """Handle update task flow"""
        task_id = int(input("\nEnter task ID to update: "))
        task = self.manager.get_task(task_id)
        
        if not task:
            self.display.print_error("Task not found!")
            return
        
        self.display.print_task(task)
        
        print("\nWhat to update?")
        print("1. Title")
        print("2. Description")
        print("3. Priority")
        print("4. Category")
        print("5. Status")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            new_title = input("New title: ").strip()
            self.manager.update_task(task_id, title=new_title)
        elif choice == '2':
            new_desc = input("New description: ").strip()
            self.manager.update_task(
                task_id,
                description=new_desc
            )
        elif choice == '3':
            new_priority = self.get_priority()
            self.manager.update_task(
                task_id,
                priority=new_priority
            )
        elif choice == '4':
            new_category = input("New category: ").strip()
            self.manager.update_task(
                task_id,
                category=new_category
            )
        elif choice == '5':
            print("\nSelect Status:")
            print("1. Pending")
            print("2. In Progress")
            print("3. Completed")
            status_choice = input("Enter choice: ").strip()
            status_map = {
                '1': Status.PENDING,
                '2': Status.IN_PROGRESS,
                '3': Status.COMPLETED
            }
            new_status = status_map.get(
                status_choice,
                Status.PENDING
            )
            self.manager.update_task(
                task_id,
                status=new_status
            )
        
        self.display.print_success("Task updated!")
    
    def search_tasks(self):
        """Handle search flow"""
        query = input("\nEnter search query: ").strip()
        results = self.manager.search_tasks(query)
        self.display.print_task_list(
            results,
            f"SEARCH RESULTS FOR '{query}'"
        )
    
    def filter_tasks(self):
        """Handle filter flow"""
        print("\nFilter by:")
        print("1. Priority")
        print("2. Category")
        print("3. Status")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            priority = self.get_priority()
            tasks = self.manager.filter_by_priority(priority)
            self.display.print_task_list(
                tasks,
                f"{priority.value.upper()} PRIORITY TASKS"
            )
        elif choice == '2':
            category = input("Enter category: ").strip()
            tasks = self.manager.filter_by_category(category)
            self.display.print_task_list(
                tasks,
                f"CATEGORY: {category.upper()}"
            )
        elif choice == '3':
            print("\nSelect Status:")
            print("1. Pending")
            print("2. In Progress")
            print("3. Completed")
            status_map = {
                '1': Status.PENDING,
                '2': Status.IN_PROGRESS,
                '3': Status.COMPLETED
            }
            status_choice = input("Enter choice: ").strip()
            status = status_map.get(
                status_choice,
                Status.PENDING
            )
            tasks = self.manager.filter_by_status(status)
            self.display.print_task_list(
                tasks,
                f"{status.value.upper()} TASKS"
            )
    
    def run(self):
        """Main application loop"""
        self.display.print_header()
        
        while True:
            self.display.print_menu()
            choice = input("\nEnter choice: ").strip()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_all_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                task_id = int(input("\nEnter task ID: "))
                self.manager.complete_task(task_id)
            elif choice == '5':
                task_id = int(input("\nEnter task ID: "))
                self.manager.delete_task(task_id)
            elif choice == '6':
                self.search_tasks()
            elif choice == '7':
                self.filter_tasks()
            elif choice == '8':
                stats = self.manager.get_statistics()
                self.display.print_statistics(stats)
            elif choice == '9':
                overdue = self.manager.get_overdue_tasks()
                self.display.print_task_list(
                    overdue,
                    "OVERDUE TASKS"
                )
            elif choice == '0':
                self.display.print_success(
                    "Thank you for using Task Manager!"
                )
                break
            else:
                self.display.print_error(
                    "Invalid choice! Please try again."
                )


if __name__ == "__main__":
    from datetime import datetime
    app = TaskManagerApp()
    app.run()
