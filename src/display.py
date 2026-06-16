from datetime import datetime
from task import Priority, Status

class DisplayManager:
    """
    Handles all CLI display and formatting
    for the Task Manager application.
    
    Author: Jajitha
    Course: Python Project Development
    """
    
    # CLI Color codes
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'reset': '\033[0m'
    }
    
    def color(self, text, color):
        """Apply color to text"""
        return (
            f"{self.COLORS.get(color, '')}"
            f"{text}"
            f"{self.COLORS['reset']}"
        )
    
    def print_header(self):
        """Print application header"""
        print("\n" + "="*50)
        print(self.color(
            "       TASK MANAGER CLI APPLICATION",
            'cyan'
        ))
        print(self.color(
            "          Author: Jajitha",
            'purple'
        ))
        print("="*50)
    
    def print_menu(self):
        """Print main menu"""
        print(self.color("\nMAIN MENU", 'bold'))
        print("-"*30)
        options = [
            "1. Add New Task",
            "2. View All Tasks",
            "3. Update Task",
            "4. Complete Task",
            "5. Delete Task",
            "6. Search Tasks",
            "7. Filter Tasks",
            "8. View Statistics",
            "9. View Overdue Tasks",
            "0. Exit"
        ]
        for option in options:
            print(self.color(option, 'white'))
        print("-"*30)
    
    def print_task(self, task):
        """Print single task with formatting"""
        priority_colors = {
            Priority.HIGH: 'red',
            Priority.MEDIUM: 'yellow',
            Priority.LOW: 'green'
        }
        
        status_colors = {
            Status.PENDING: 'yellow',
            Status.IN_PROGRESS: 'blue',
            Status.COMPLETED: 'green'
        }
        
        priority_color = priority_colors.get(
            task.priority, 'white'
        )
        status_color = status_colors.get(
            task.status, 'white'
        )
        
        print("\n" + "-"*45)
        print(f"ID: {self.color(str(task.id), 'cyan')}")
        print(f"Title: {self.color(task.title, 'bold')}")
        
        if task.description:
            print(f"Description: {task.description}")
        
        print(f"Priority: {self.color(task.priority.value, priority_color)}")
        print(f"Status: {self.color(task.status.value, status_color)}")
        print(f"Category: {task.category}")
        
        if task.deadline:
            days = task.days_until_deadline()
            if task.is_overdue():
                deadline_str = self.color(
                    f"OVERDUE by {abs(days)} days!",
                    'red'
                )
            else:
                deadline_str = self.color(
                    f"Due in {days} days",
                    'green'
                )
            print(f"Deadline: {deadline_str}")
        
        print(f"Created: {task.created_at[:10]}")
        
        if task.completed_at:
            print(f"Completed: {task.completed_at[:10]}")
    
    def print_task_list(self, tasks, title="ALL TASKS"):
        """Print list of tasks"""
        print(f"\n{self.color(title, 'cyan')}")
        print("="*50)
        
        if not tasks:
            print(self.color(
                "No tasks found!",
                'yellow'
            ))
            return
        
        print(f"Total: {len(tasks)} tasks\n")
        for task in tasks:
            self.print_task(task)
        
        print("\n" + "="*50)
    
    def print_statistics(self, stats):
        """Print task statistics"""
        print(f"\n{self.color('TASK STATISTICS', 'cyan')}")
        print("="*50)
        
        if stats.get('total', 0) == 0:
            print(self.color("No tasks yet!", 'yellow'))
            return
        
        print(f"Total Tasks: {self.color(str(stats['total']), 'bold')}")
        print(f"Completed: {self.color(str(stats['completed']), 'green')}")
        print(f"In Progress: {self.color(str(stats['in_progress']), 'blue')}")
        print(f"Pending: {self.color(str(stats['pending']), 'yellow')}")
        print(f"Overdue: {self.color(str(stats['overdue']), 'red')}")
        print(f"High Priority: {self.color(str(stats['high_priority']), 'red')}")
        print(f"Completion Rate: {self.color(stats['completion_rate'], 'green')}")
        
        if stats.get('categories'):
            print(f"\n{self.color('BY CATEGORY:', 'purple')}")
            for category, count in stats['categories'].items():
                print(f"  {category}: {count} tasks")
        
        print("="*50)
    
    def print_success(self, message):
        """Print success message"""
        print(self.color(f"✅ {message}", 'green'))
    
    def print_error(self, message):
        """Print error message"""
        print(self.color(f"❌ {message}", 'red'))
    
    def print_warning(self, message):
        """Print warning message"""
        print(self.color(f"⚠️  {message}", 'yellow'))


if __name__ == "__main__":
    display = DisplayManager()
    display.print_header()
    display.print_menu()
    print("\nDisplay Manager initialized successfully!")
