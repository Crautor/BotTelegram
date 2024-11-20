from django.db import models

class Product(models.Model):
    category = models.ForeignKey('Category', related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    photo_url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
