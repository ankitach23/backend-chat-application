from django.db import models
from django.contrib.auth.models import User as DjangoUser

class ChatUser(models.Model):
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    # Add other fields like username, email, etc.
    online = models.BooleanField(default=False)
    class Meta:
        managed = True  # Set managed to True for your custom models
        db_table = 'chatapp_user'

    def __str__(self):
        return self.django_user.username  # Customize how users are displayed

class Message(models.Model):
    sender = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = True  # Set managed to True for your custom models
        db_table = 'chatapp_message'

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content}"  # Customize message representation
