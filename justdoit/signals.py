from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Todo

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey('Todo', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.todo.title}"
    
@receiver(post_save, sender=Todo)
def create_todo_notification(sender, instance, created, **kwargs):
    if created:
        #notify assigned user
        if instance.assigned_to:
            Notification.objects.create(
                user = instance.assigned_to,
                todo = instance,
                message = f"New task assigned: {instance.title}"
            )

        else:
            #notify on status change or important updates
            if instance.assigned_to:
                Notification.objects.create(
                    user = instance.assigned_to,
                    todo = instance,
                    message = f"Task status updated: {instance.title}"
                )

