from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="users/", blank=True, null=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# class ChatroomManager(models.Manager):
#     def is_exists(self, chatroom_id):
#         return self.filter(
#         )


class Chatrooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    is_deleted = models.BooleanField(default=False)
    users = models.ManyToManyField(Profiles, related_name="users")
    admins = models.ManyToManyField(Profiles, related_name="admins")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('chat:room', kwargs={'room_id': self.id})


class Messages(models.Model):
    sender = models.ForeignKey(Profiles, on_delete=models.SET_NULL, null=True)
    # sender = models.OneToOneField(Profiles, on_delete=models.SET_NULL, blank=True, null=True)
    reciever_id = models.CharField(max_length=40)
    RECIEVER_TYPE_CHOICES = [
        (1, 'Chatroom'),
        (2, 'User'),
    ]
    reciever_type = models.IntegerField(
        choices=RECIEVER_TYPE_CHOICES,
        default=1,
    )
    message = models.TextField()
    MESSAGE_TYPE_CHOICE = [
        (1, "Text"),
        (2, "File"),
    ]
    message_type = models.IntegerField(
        choices=MESSAGE_TYPE_CHOICE,
        default=1
    )
    send_datetime = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    seen_datetime = models.DateTimeField(null=True)
    is_reply = models.OneToOneField('self', on_delete=models.SET_NULL, blank=True, null=True)
    sender_deleted = models.BooleanField(default=False)
    reciever_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message


class MessageFiles(models.Model):
    file = models.FileField(upload_to="messagefiles/")
    message = models.OneToOneField(Messages, on_delete = models.CASCADE)

