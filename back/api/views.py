from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models.user_model import User
from api.models.category_model import Category
from api.models.client_model import Client
from api.models.message_model import Message
from api.models.order_item_model import OrderItem
from api.models.order_model import Order
from api.models.product_model import Product

from .serializers import UserSerializer
from .serializers import CategorySerializer
from .serializers import ClientSerializer
from .serializers import MessageSerializer
from .serializers import OrderItemSerializer
from .serializers import OrderSerializer
from .serializers import ProductSerializer

@api_view(['GET'])
def getUsers(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUserByID(request, id):
  try:
    data = User.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

  if request.method == 'GET':
    serializer = UserSerializer(data)
    return Response(serializer.data)
  return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createUser(request):
  if request.method == 'POST':
    new_user = request.data

    serializer = UserSerializer(data=new_user)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateUser(request, id):
  try:
    data = User.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'PUT':
    print(data)
    serializer = UserSerializer(data, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteUser(request, id):
  try:
    data = User.objects.get(id=id)
    data.delete()
    return Response(status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

@api_view(['GET'])
def getCategories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getCategoryByID(request, id):
  try:
    data = Category.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

  if request.method == 'GET':
    serializer = CategorySerializer(data)
    return Response(serializer.data)
  return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createCategory(request):
  if request.method == 'POST':
    new_category = request.data

    serializer = CategorySerializer(data=new_category)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['PUT'])
def updateCategory(request, id):
  try:
    data = Category.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'PUT':
    print(data)
    serializer = CategorySerializer(data, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteCategory(request, id):
  try:
    data = Category.objects.get(id=id)
    data.delete()
    return Response(status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

@api_view(['GET'])
def getClients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getClientByID(request, id):
  try:
    data = Client.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

  if request.method == 'GET':
    serializer = ClientSerializer(data)
    return Response(serializer.data)
  return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createClient(request):
  if request.method == 'POST':
    new_client = request.data

    serializer = ClientSerializer(data=new_client)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['PUT'])
def updateClient(request, id):
  try:
    data = Client.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'PUT':
    print(data)
    serializer = ClientSerializer(data, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteClient(request, id):
  try:
    data = Client.objects.get(id=id)
    data.delete()
    return Response(status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

@api_view(['GET'])
def getMessages(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getMessageByID(request, id):
  try:
    data = Message.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

  if request.method == 'GET':
    serializer = MessageSerializer(data)
    return Response(serializer.data)
  return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createMessage(request):
  if request.method == 'POST':
    new_message = request.data

    serializer = MessageSerializer(data=new_message)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['PUT'])
def updateMessage(request, id):
  try:
    data = Message.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'PUT':
    print(data)
    serializer = MessageSerializer(data, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteMessage(request, id):
  try:
    data = Message.objects.get(id=id)
    data.delete()
    return Response(status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

@api_view(['GET'])
def getOrderItems(request):
    if request.method == 'GET':
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getOrderItemByID(request, id):
  try:
    data = OrderItem.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

  if request.method == 'GET':
    serializer = OrderItemSerializer(data)
    return Response(serializer.data)
  return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createOrderItem(request):
  if request.method == 'POST':
    new_order_item = request.data

    serializer = OrderItemSerializer(data=new_order_item)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['PUT'])
def updateOrderItem(request, id):
  try:
    data = OrderItem.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'PUT':
    print(data)
    serializer = OrderItemSerializer(data, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteOrderItem(request, id):
  try:
    data = OrderItem.objects.get(id=id)
    data.delete()
    return Response(status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
@api_view(['GET'])
def getOrderItemsByOrderID(request, id):
    if request.method == 'GET':
        order_items = OrderItem.objects.filter(order=id)
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getOrders(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getOrderByID(request, id):
  try:
    data = Order.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  

  if request.method == 'GET':
    serializer = OrderSerializer(data)
    return Response(serializer.data)
  return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createOrder(request):
  if request.method == 'POST':
    new_order = request.data

    serializer = OrderSerializer(data=new_order)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['PUT'])
def updateOrder(request, id):
  try:
    data = Order.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'PUT':
    print(data)
    serializer = OrderSerializer(data, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteOrder(request, id):
  try:
    data = Order.objects.get(id=id)
    data.delete()
    return Response(status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getProducts(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getProductById(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createProduct(request):
  if request.method == 'POST':
    new_product = request.data

    serializer = ProductSerializer(data=new_product)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['PUT'])
def updateProduct(request, id):
  try:
    data = Product.objects.get(id=id)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'PUT':
    print(data)
    serializer = ProductSerializer(data, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteProduct(request, id):
  try:
    data = Product.objects.get(id=id)
    data.delete()
    return Response(status=status.HTTP_200_OK)
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
@api_view(['GET'])
def getProductsByCategory(request, category_id):
    if request.method == 'GET':
        products = Product.objects.filter(category=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

