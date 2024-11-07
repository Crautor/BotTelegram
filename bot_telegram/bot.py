import os
import httpx
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Função auxiliar para obter orders do usuário
async def get_user_orders(user_id):
    url = f"http://localhost:8000/api/order/user/{user_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Função auxiliar para obter categorias
async def get_categories():
    url = "http://localhost:8000/api/category/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Função auxiliar para obter detalhes de um order
async def get_order_details(order_id):
    url = f"http://localhost:8000/api/order/{order_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Função auxiliar para obter produtos de uma categoria
async def get_products_by_category(category_id):
    url = f"http://localhost:8000/api/product/category/{category_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    
async def get_cart_by_id():
    url = f"http://localhost:8000/api/cart/`"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    
async def get_product_details_by_id(product_id):
    url = f"http://localhost:8000/api/product/{product_id}"  # Ajuste a URL conforme sua API.
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()  # Retorna os detalhes do produto (ex: nome, preço, etc.)

# Função para listar orders do usuário
async def listar_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id  # Obtém o ID do usuário
    try:
        orders = await get_user_orders(user_id)

        if isinstance(orders, list) and orders:
            keyboard = [[InlineKeyboardButton(f'Order {order["id"]}', callback_data=f'order_{order["id"]}') for order in orders]]
            keyboard.append([InlineKeyboardButton("Voltar", callback_data="Voltar")])
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Verifica se é uma mensagem de callback ou uma mensagem regular e responde adequadamente
            if update.callback_query:
                await update.callback_query.edit_message_text("Escolha um order:", reply_markup=reply_markup)
            else:
                await update.message.reply_text("Escolha um order:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Nenhum pedido ativo encontrado.")
    except httpx.HTTPStatusError as exc:
        await update.message.reply_text(f"Erro ao obter orders: {exc.response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Erro inesperado: {str(e)}")

# Função para iniciar o bot com opções iniciais
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Orders", callback_data="orders"), 
         InlineKeyboardButton("Categorias", callback_data="Categorias"),
         InlineKeyboardButton("Ver Carrinho", callback_data="view_cart")],
        [InlineKeyboardButton("Voltar", callback_data="Voltar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.answer()
        await query.edit_message_text("Escolha uma opção:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Escolha uma opção:", reply_markup=reply_markup)


async def tratar_botao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Verificar se há uma mensagem associada ao callback_query
    if query.message:
        try:
            # Verifique qual foi a opção selecionada e execute a ação correspondente
            if query.data == "orders":
                await listar_orders(update, context)
            elif query.data == "Categorias":
                await listar_categorias(query, context)
            elif query.data.startswith('order_'):
                order_id = query.data.split('_')[1]
                await mostrar_order(query, order_id)
            elif query.data.startswith('category_'):
                category_id = query.data.split('_')[1]
                await listar_produtos(query, category_id, context)
            elif query.data == "Voltar":
                await iniciar(update, context)
            else:
                # Para opções não reconhecidas, edite a mensagem com a opção selecionada
                await query.edit_message_text(text=f"Opção selecionada: {query.data}")
        except telegram.error.BadRequest as e:
            # Caso não seja possível editar a mensagem (por exemplo, não há texto na mensagem), envie uma nova mensagem
            await query.message.reply_text(f"Opção selecionada: {query.data}")
        except Exception as e:
            # Em caso de outros erros, envie uma mensagem de erro genérica
            await query.message.reply_text(f"Ocorreu um erro: {str(e)}")
    else:
        # Se não houver uma mensagem para editar, envie uma nova mensagem
        await update.message.reply_text(f"Opção selecionada: {query.data}")


async def ver_carrinho(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id  # Obtém o ID do usuário
    
    # Chama a API para buscar o carrinho ativo do cliente
    url = f"http://localhost:8000/api/cart/{user_id}/"
    
    try:
        # Faz a requisição para o backend Django
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Lança exceção para erros HTTP
            cart_data = response.json()  # Obtém os dados do carrinho
            
            # Verifica se o carrinho tem itens
            if cart_data.get('cart_items'):
                texto_carrinho = "Produtos no seu carrinho:\n\n"
                for item in cart_data['cart_items']:
                    product_name = item['product']['name']
                    quantity = item['quantity']
                    price = item['product']['price']
                    texto_carrinho += f"{product_name} - {quantity} x R${price}\n"
                
                keyboard = [
                    [InlineKeyboardButton("Finalizar Pedido", callback_data="finalizar_pedido")],
                    [InlineKeyboardButton("Voltar", callback_data="Voltar")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.callback_query.edit_message_text(texto_carrinho, reply_markup=reply_markup)
            else:
                await update.callback_query.edit_message_text("Seu carrinho está vazio.", reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Voltar", callback_data="Voltar")]]))
    
    except httpx.HTTPStatusError as exc:
        await update.callback_query.edit_message_text(f"Erro ao obter o carrinho: {exc.response.status_code}")
    except Exception as e:
        await update.callback_query.edit_message_text(f"Erro inesperado: {str(e)}")
    
    # Verifica se o carrinho não está vazio
    carrinho = context.user_data.get('carrinho', [])
    if not carrinho:
        await update.callback_query.edit_message_text("Seu carrinho está vazio. Não é possível finalizar o pedido.")
        return
    
    # Pergunta o nome
    await update.callback_query.edit_message_text("Por favor, informe seu nome completo.")
    return await ask_for_name(update, context)

# Função que pergunta o nome do cliente
async def ask_for_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    context.user_data['step'] = 'name'  # Marca o passo como nome
    await update.message.reply_text("Qual o seu nome completo?")

# Função que coleta o nome e pede o endereço
async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    step = context.user_data.get('step')
    
    if step == 'name':
        # Armazena o nome
        context.user_data['name'] = update.message.text
        await update.message.reply_text("Agora, informe seu endereço completo.")
        context.user_data['step'] = 'address'  # Marca o passo como endereço
    elif step == 'address':
        # Armazena o endereço
        context.user_data['address'] = update.message.text
        await update.message.reply_text(f"Você informou o endereço: {update.message.text}. Está correto? (Sim/Não)")
        context.user_data['step'] = 'confirm_address'

async def confirm_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    answer = update.message.text.lower()
    
    if answer == 'sim':
        # Criação do pedido
        name = context.user_data.get('name')
        address = context.user_data.get('address')
        user_id_telegram = update.effective_user.id
        
        # Chama a API para criar o pedido
        order_data = {
            'user_id': user_id_telegram,
            'name': name,
            'address': address,
            'products': context.user_data.get('carrinho', [])
        }
        # Envia os dados para a API para criar o pedido
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/api/order", json=order_data)
                response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            await update.message.reply_text("Seu pedido foi realizado com sucesso!")
        except httpx.HTTPStatusError as exc:
            await update.message.reply_text(f"Erro ao realizar o pedido: {exc.response.status_code}")
        
        # Limpa o carrinho
        context.user_data['carrinho'] = []
    else:
        await update.message.reply_text("Por favor, forneça um novo endereço.")
        context.user_data['step'] = 'address'  # Retorna ao passo de endereço    

# Função para listar categorias
async def listar_categorias(query, context):
    try:
        categories = await get_categories()

        if isinstance(categories, list) and categories:
            keyboard = [[InlineKeyboardButton(category["name"], callback_data=f'category_{category["id"]}') for category in categories]]
            keyboard.append([InlineKeyboardButton("Voltar", callback_data="Voltar")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Escolha uma categoria:", reply_markup=reply_markup)
        else:
            await query.edit_message_text("Nenhuma categoria encontrada.")
    except httpx.HTTPStatusError as exc:
        await query.edit_message_text(f"Erro ao obter categorias: {exc.response.status_code}")
    except Exception as e:
        await query.edit_message_text(f"Erro inesperado: {str(e)}")

# Função para listar produtos de uma categoria
async def listar_produtos(query, category_id, context):
    try:
        products = await get_products_by_category(category_id)

        if isinstance(products, list) and products:
            for product in products:
                image_url = product.get("photo_url") or product.get("image")
                
                keyboard = [
                    [InlineKeyboardButton("Adicionar ao Carrinho", callback_data=f'add_to_cart_{product["id"]}')],
                    [InlineKeyboardButton("Voltar", callback_data="Voltar")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                if image_url:
                    await context.bot.send_photo(
                        chat_id=query.message.chat.id,
                        photo=image_url,
                        caption=f'{product["name"]}',
                        reply_markup=reply_markup
                    )
                else:
                    await query.edit_message_text("URL da imagem não encontrada para o produto.")
        else:
            await query.edit_message_text("Nenhum produto encontrado na categoria.")
    except httpx.HTTPStatusError as exc:
        await query.edit_message_text(f"Erro ao obter produtos da categoria: {exc.response.status_code}")
    except Exception as e:
        await query.edit_message_text(f"Erro inesperado: {str(e)}")

# Função para adicionar um produto ao carrinho
async def adicionar_ao_carrinho(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extrair o ID do produto da callback_data
    product_id = update.callback_query.data.split('_')[2]
    
    # Buscar os detalhes do produto (você precisará buscar o nome e preço)
    product_details = await get_product_details_by_id(product_id)  # Implementar esta função para buscar os detalhes do produto.
    
    # Adicionar o produto ao carrinho do usuário (armazenado em context.user_data)
    context.user_data.setdefault('carrinho', []).append({
        'product_id': product_id,
        'name': product_details['name'],
        'price': product_details['price']
    })
    
    # Responder ao usuário com uma mensagem
    await update.callback_query.answer(f"Produto {product_details['name']} adicionado ao carrinho!")
    
    # Optionally, show the current contents of the cart
    await ver_carrinho(update, context)


# Configuração do token do bot e inicialização do aplicativo
BOT_TOKEN = os.getenv("BOT_TOKEN","7327581607:AAHG84Ie_4dR8LPSxkGP_ZAEZVZtD4NGYyw")
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Registro dos handlers
app.add_handler(CommandHandler("listar_orders", listar_orders))
app.add_handler(CommandHandler("iniciar", iniciar))
app.add_handler(CallbackQueryHandler(tratar_botao))

# Execução do bot
app.run_polling()
