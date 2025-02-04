from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

class Profile(models.Model):
    ROLE_CHOICES = [
        ('MANAGER', 'Project Manager'),
        ('MEMBER', 'Team Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        default='default_profile.png', 
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='MEMBER'
    )
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.height >300 or img.width > 300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)