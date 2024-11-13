from django.db import models

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='cart_items', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"
