from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    telegram_user_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
