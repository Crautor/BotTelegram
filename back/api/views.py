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
from api.models.cart_model import Cart
from api.models.cart_item_model import CartItem
from api.models.address_model import Address


from .serializers import UserSerializer
from .serializers import CategorySerializer
from .serializers import ClientSerializer
from .serializers import MessageSerializer
from .serializers import OrderItemSerializer
from .serializers import OrderSerializer
from .serializers import ProductSerializer
from .serializers import CartItemSerializer
from .serializers import CartSerializer
from .serializers import AddressSerializer


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

@api_view(['GET'])
def getClientByTelegramID(request, telegram_user_id):
    try:
        # Busca pelo telegram_user_id no banco de dados
        client = Client.objects.get(telegram_user_id=telegram_user_id)
    except Client.DoesNotExist:
        return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = ClientSerializer(client)
    return Response(serializer.data, status=status.HTTP_200_OK)


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


@api_view(['GET'])
def getCart(request):
    if request.method == 'GET':
        products = Cart.objects.all()
        serializer = CartSerializer(products, many=True)  # Passa o queryset 'products'
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getCartById(request, client_id):
    try:
        cart = Cart.objects.get(client_id=client_id, is_active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def addToCart(request, client_id):
    try:
        client = Client.objects.get(id=client_id)  # Verifica se o cliente existe
    except Client.DoesNotExist:
        return Response({"error": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)  # Padrão de quantidade: 1

    try:
        product = Product.objects.get(id=product_id)  # Verifica se o produto existe
    except Product.DoesNotExist:
        return Response({"error": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Obtém ou cria o carrinho ativo do cliente
    cart, created = Cart.objects.get_or_create(client=client, is_active=True)

    # Tenta encontrar o item do carrinho
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    cart_item.save()

    return Response({
        "message": "Produto adicionado ao carrinho com sucesso",
        "cart_id": cart.id,
        "product_id": product.id,
        "quantity": cart_item.quantity
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def updateCartItem(request, client_id, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__client_id=client_id)
    except CartItem.DoesNotExist:
        return Response({"detail": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get('quantity')
    
    # Verifica se a quantidade é válida
    if quantity is not None and quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        return Response({"detail": "Cart item updated"}, status=status.HTTP_200_OK)

    return Response({"detail": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def removeFromCart(request, client_id, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__client_id=client_id)
        cart_item.delete()
        return Response({"detail": "Item removed from cart"}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({"detail": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def checkout(request, client_id):
    try:
        cart = Cart.objects.get(client_id=client_id, is_active=True)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    # Aqui você pode criar um pedido com os itens do carrinho, por exemplo
    # Vamos criar uma ordem com base nos itens do carrinho (você pode adicionar mais lógica conforme necessário)
    order = Order.objects.create(client=cart.client, status="pending", amount=cart.total_amount())  # O método `total_amount()` seria uma função que calcula o total com base nos itens do carrinho.

    # Crie a ordem a partir dos itens no carrinho
    for item in cart.cart_items.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

    # Após finalizar a compra, podemos desativar o carrinho
    cart.is_active = False
    cart.save()

    return Response({"detail": "Order created from cart"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getAddress(request):
    addresses = Address.objects.all()
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'DELETE'])
def getdelAddressById(request, pk):
    """
    Recupera, exclui ou retorna erro 404 se o endereço com ID específico não for encontrado.
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return Response({'error': 'Endereço não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# POST - Criação de novo endereço
@api_view(['POST'])
def createAddress(request):
    """
    Cria um novo endereço.
    """
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUT - Atualização do endereço existente
@api_view(['PUT'])
def updateAddress(request, pk):
    """
    Atualiza o endereço existente pelo ID.
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return Response({'error': 'Endereço não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AddressSerializer(address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getCartItems(request, client_id):
    try:
        # Localizar o cliente
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"error": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Localizar o carrinho ativo
        cart = Cart.objects.get(client=client, is_active=True)
    except Cart.DoesNotExist:
        return Response({"error": "Carrinho ativo não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Obter os itens do carrinho
    items = CartItem.objects.filter(cart=cart)
    serializer = CartItemSerializer(items, many=True)

    return Response({
        "cart_id": cart.id,
        "items": serializer.data
    }, status=status.HTTP_200_OK)
