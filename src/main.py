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
