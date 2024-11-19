from django.db import models

class Address(models.Model):
    phone_number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)

    def __str__(self):
        return self.name
