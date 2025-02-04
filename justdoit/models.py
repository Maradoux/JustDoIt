from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile


# Create your models here.
class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=False, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='pending')
    completed = models.BooleanField(default=False)

    #User creation
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= 'created_todos')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_todos')

    def __str__(self):
        return f"{self.title} - Assigned to: {self.assigned_to.username if self.assigned_to else 'Unassigned'}"
    
    class Meta:
        ordering = ['-created_date']

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey('Todo', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.todo.title}"
    