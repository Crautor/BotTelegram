from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('user/', views.getUsers, name='getAll'),
    path('user/<int:id>', views.getUserByID, name='getByID'),
    path('user/create/', views.createUser, name='createUser'),
    path('user/update/<int:id>', views.updateUser, name='updateUser'),
    path('user/delete/<int:id>', views.deleteUser, name='deleteUser'),
    path('category/', views.getCategories, name='getAll'),
    path('category/<int:id>', views.getCategoryByID, name='getByID'),
    path('category/create/', views.createCategory, name='createCategory'),
    path('category/update/<int:id>', views.updateCategory, name='updateCategory'),
    path('category/delete/<int:id>', views.deleteCategory, name='deleteCategory'),
    path('product/', views.getProducts, name='getAll'),
    path('product/<int:id>', views.getProductById, name='getByID'),
    path('product/create/', views.createProduct, name='createProduct'),
    path('product/update/<int:id>', views.updateProduct, name='updateProduct'),
    path('product/delete/<int:id>', views.deleteProduct, name='deleteProduct'),
    path('order/', views.getOrders, name='getAll'),
    path('order/<int:id>', views.getOrderByID, name='getByID'),
    path('order/create/', views.createOrder, name='createOrder'),
    path('order/update/<int:id>', views.updateOrder, name='updateOrder'),
    path('order/delete/<int:id>', views.deleteOrder, name='deleteOrder'),
    path('orderitem/', views.getOrderItems, name='getAll'),
    path('orderitem/<int:id>', views.getOrderItemByID, name='getByID'),
    path('orderitem/create/', views.createOrderItem, name='createOrderItem'),
    path('orderitem/update/<int:id>', views.updateOrderItem, name='updateOrderItem'),
    path('orderitem/delete/<int:id>', views.deleteOrderItem, name='deleteOrderItem'),
    path('orderitem/order/<int:id>', views.getOrderItemsByOrderID, name='getByOrderID'),
    path('client/', views.getClients, name='getAll'),
    path('client/<int:id>', views.getClientByID, name='getByID'),
    path('client/create/', views.createClient, name='createClient'),
    path('client/update/<int:id>', views.updateClient, name='updateClient'),
    path('client/delete/<int:id>', views.deleteClient, name='deleteClient'),
    

]