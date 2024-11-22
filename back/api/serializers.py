from rest_framework import serializers

from api.models.user_model import User
from api.models.category_model import Category
from api.models.client_model import Client
from api.models.message_model import Message
from api.models.order_item_model import OrderItem
from api.models.order_model import Order
from api.models.product_model import Product
from api.models.cart_model import Cart
from api.models.cart_item_model import CartItem




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)  # Relaciona os itens do carrinho com o carrinho

    class Meta:
        model = Cart
        fields = '__all__'





