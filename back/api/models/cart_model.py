from django.db import models

class Cart(models.Model):
    client = models.ForeignKey('Client', related_name='carts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # Para indicar se o carrinho está ativo ou finalizado

    def __str__(self):
        return f"Cart {self.id} - {self.client.name}"
