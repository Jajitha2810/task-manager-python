import json
import os
from datetime import datetime
from task import Task, Priority, Status

class TaskManager:
    """
    Core Task Manager handling all CRUD operations
    with JSON data persistence.
    
    Author: Jajitha
    Course: Python Project Development
    """
    
    def __init__(self, data_file='data/tasks.json'):
        self.data_file = data_file
        self.tasks = {}
        self.next_id = 1
        self._ensure_data_directory()
        self._load_tasks()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(
            os.path.dirname(self.data_file),
            exist_ok=True
        )
    
    def _load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = {
                        int(k): Task.from_dict(v)
                        for k, v in data['tasks'].items()
                    }
                    self.next_id = data.get('next_id', 1)
                print(f"Loaded {len(self.tasks)} tasks!")
            except Exception as e:
                print(f"Error loading tasks: {e}")
                self.tasks = {}
    
    def _save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = {
                'tasks': {
                    str(k): v.to_dict()
                    for k, v in self.tasks.items()
                },
                'next_id': self.next_id,
                'last_saved': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(
        self,
        title,
        description="",
        priority=Priority.MEDIUM,
        category="General",
        deadline=None
    ):
        """Add a new task"""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            category=category,
            deadline=deadline
        )
        task.id = self.next_id
        self.tasks[self.next_id] = task
        self.next_id += 1
        self._save_tasks()
        print(f"Task '{title}' added successfully! ID: {task.id}")
        return task
    
    def get_task(self, task_id):
        """Get task by ID"""
        task = self.tasks.get(task_id)
        if not task:
            print(f"Task {task_id} not found!")
        return task
    
    def get_all_tasks(self):
        """Get all tasks"""
        return list(self.tasks.values())
    
    def update_task(self, task_id, **kwargs):
        """Update task fields"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = datetime.now().isoformat()
        self._save_tasks()
        print(f"Task {task_id} updated successfully!")
        return task
    
    def delete_task(self, task_id):
        """Delete task by ID"""
        if task_id in self.tasks:
            title = self.tasks[task_id].title
            del self.tasks[task_id]
            self._save_tasks()
            print(f"Task '{title}' deleted successfully!")
            return True
        print(f"Task {task_id} not found!")
        return False
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        task = self.get_task(task_id)
        if task:
            task.complete()
            self._save_tasks()
            print(f"Task '{task.title}' marked as completed!")
        return task
    
    def search_tasks(self, query):
        """Search tasks by title or description"""
        query = query.lower()
        results = [
            task for task in self.tasks.values()
            if query in task.title.lower()
            or query in task.description.lower()
        ]
        return results
    
    def filter_by_priority(self, priority):
        """Filter tasks by priority"""
        return [
            task for task in self.tasks.values()
            if task.priority == priority
        ]
    
    def filter_by_category(self, category):
        """Filter tasks by category"""
        return [
            task for task in self.tasks.values()
            if task.category.lower() == category.lower()
        ]
    
    def filter_by_status(self, status):
        """Filter tasks by status"""
        return [
            task for task in self.tasks.values()
            if task.status == status
        ]
    
    def get_overdue_tasks(self):
        """Get all overdue tasks"""
        return [
            task for task in self.tasks.values()
            if task.is_overdue()
        ]
    
    def get_statistics(self):
        """Calculate task statistics"""
        total = len(self.tasks)
        if total == 0:
            return {'total': 0}
        
        completed = len([
            t for t in self.tasks.values()
            if t.status == Status.COMPLETED
        ])
        in_progress = len([
            t for t in self.tasks.values()
            if t.status == Status.IN_PROGRESS
        ])
        pending = len([
            t for t in self.tasks.values()
            if t.status == Status.PENDING
        ])
        overdue = len(self.get_overdue_tasks())
        
        high_priority = len([
            t for t in self.tasks.values()
            if t.priority == Priority.HIGH
        ])
        
        categories = {}
        for task in self.tasks.values():
            categories[task.category] = (
                categories.get(task.category, 0) + 1
            )
        
        return {
            'total': total,
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'overdue': overdue,
            'high_priority': high_priority,
            'completion_rate': f"{(completed/total)*100:.1f}%",
            'categories': categories
        }


if __name__ == "__main__":
    manager = TaskManager()
    
    # Example usage
    manager.add_task(
        title="Complete TOPIK Study Guide",
        description="Study chapters 1-10",
        priority=Priority.HIGH,
        category="Education",
        deadline="2026-12-01T00:00:00"
    )
    
    manager.add_task(
        title="Submit GKS Application",
        description="Prepare all documents",
        priority=Priority.HIGH,
        category="Application"
    )
    
    stats = manager.get_statistics()
    print(f"\nStatistics: {stats}")
