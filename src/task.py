from datetime import datetime
from enum import Enum

class Priority(Enum):
    """Task priority levels"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Status(Enum):
    """Task status options"""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class Task:
    """
    Represents a single task in the task manager.
    
    Author: Jajitha
    Course: Python Project Development
    """
    
    def __init__(
        self,
        title,
        description="",
        priority=Priority.MEDIUM,
        category="General",
        deadline=None
    ):
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.status = Status.PENDING
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.deadline = deadline
        self.completed_at = None
    
    def complete(self):
        """Mark task as completed"""
        self.status = Status.COMPLETED
        self.completed_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def start(self):
        """Mark task as in progress"""
        self.status = Status.IN_PROGRESS
        self.updated_at = datetime.now().isoformat()
    
    def is_overdue(self):
        """Check if task is overdue"""
        if self.deadline and self.status != Status.COMPLETED:
            deadline_date = datetime.fromisoformat(self.deadline)
            return datetime.now() > deadline_date
        return False
    
    def days_until_deadline(self):
        """Calculate days remaining until deadline"""
        if self.deadline:
            deadline_date = datetime.fromisoformat(self.deadline)
            delta = deadline_date - datetime.now()
            return delta.days
        return None
    
    def to_dict(self):
        """Convert task to dictionary for JSON storage"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'category': self.category,
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deadline': self.deadline,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary"""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority(data.get('priority', 'Medium')),
            category=data.get('category', 'General'),
            deadline=data.get('deadline')
        )
        task.id = data['id']
        task.status = Status(data.get('status', 'Pending'))
        task.created_at = data.get('created_at')
        task.updated_at = data.get('updated_at')
        task.completed_at = data.get('completed_at')
        return task
    
    def __str__(self):
        deadline_str = ""
        if self.deadline:
            days = self.days_until_deadline()
            if self.is_overdue():
                deadline_str = f" | ⚠️ OVERDUE by {abs(days)} days"
            else:
                deadline_str = f" | Due in {days} days"
        
        return (
            f"[{self.id}] {self.title} "
            f"| {self.priority.value} "
            f"| {self.status.value} "
            f"| {self.category}"
            f"{deadline_str}"
        )


if __name__ == "__main__":
    # Example usage
    task = Task(
        title="Study for TOPIK exam",
        description="Complete chapters 1-5 of Korean grammar",
        priority=Priority.HIGH,
        category="Education",
        deadline="2026-12-01T00:00:00"
    )
    
    print("Task created successfully!")
    print(task)
    print(f"\nTask details: {task.to_dict()}")
