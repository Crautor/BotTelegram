import logging
import httpx
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define stages
VIEW_CATEGORIES, VIEW_PRODUCTS, VIEW_CART, CONFIRM_ORDER, COLLECT_NAME, COLLECT_PHONE, COLLECT_ADDRESS, COLLECT_CITY = range(8)

# Define callback data
CATEGORY, PRODUCT, CART, ORDER, INCREMENT, DECREMENT, CONFIRM = range(7)

# Base API URL
BASE_API_URL = "http://back:3001/api"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the bot and show the main menu."""
    user = update.message.from_user
    telegram_user_id = user.id
    logger.info("User %s started the conversation with ID %s.", user.first_name, telegram_user_id)

    # Verifica se o client_id já foi salvo no contexto
    if 'client_id' not in context.user_data:
        async with httpx.AsyncClient() as client:
            # Tenta buscar o cliente com o telegram_user_id
            response = await client.get(f"{BASE_API_URL}/client/{telegram_user_id}/")
            
            if response.status_code == 200:
                # Cliente encontrado, pega o client_id
                context.user_data["client_id"] = response.json().get("id")
                logger.info(f"Cliente encontrado. Client ID: {context.user_data['client_id']}")
            elif response.status_code == 404:  # Caso o cliente não exista, cria um novo
                client_data = {"telegram_user_id": telegram_user_id, "name": user.first_name}
                response = await client.post(f"{BASE_API_URL}/client/create/", json=client_data)
                if response.status_code == 201:
                    response_data = response.json()
                    context.user_data["client_id"] = response_data.get("id")
                    logger.info(f"Cliente criado com sucesso. Client ID: {context.user_data['client_id']}")
                else:
                    # Se o status de criação não for 201, loga o erro
                    logger.error(f"Falha ao criar cliente: {response.status_code} - {response.text}")
                    await update.message.reply_text("Erro ao criar cliente. Tente novamente mais tarde.")
                    return ConversationHandler.END
            else:
                # Se a resposta não for nem 200 nem 404, loga o erro e interrompe
                logger.error(f"Erro ao verificar cliente: {response.status_code} - {response.text}")
                await update.message.reply_text("Erro ao verificar cliente. Tente novamente mais tarde.")
                return ConversationHandler.END
    else:
        # Se o client_id já existe, loga
        logger.info(f"Cliente já existe. Client ID: {context.user_data['client_id']}")

    # Exibe o menu inicial
    keyboard = [
        [InlineKeyboardButton("Ver Categorias", callback_data="view_categories")],
        [InlineKeyboardButton("Ver Carrinho", callback_data="view_cart")],
        [InlineKeyboardButton("Finalizar Pedido", callback_data="confirm_order")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bem-vindo! Escolha uma opção:", reply_markup=reply_markup)
    return VIEW_CATEGORIES



async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show products of a selected category."""
    query = update.callback_query
    await query.answer()
    
    category_id = query.data.split(":")[1]
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_API_URL}/product/category/{category_id}")
        if response.status_code == 200:
            products = response.json()
        else:
            await query.edit_message_text(f"Erro ao carregar produtos: {response.text}")
            return VIEW_CATEGORIES

    keyboard = [
        [InlineKeyboardButton(prod['name'], callback_data=f"{PRODUCT}:{prod['id']}")]
        for prod in products
    ]
    keyboard.append([InlineKeyboardButton("Voltar", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Escolha um produto:", reply_markup=reply_markup)
    return VIEW_PRODUCTS


async def add_product_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    product_id = query.data.split(":")[1]
    quantity = 1

    client_id = context.user_data.get('client_id')
    if not client_id:
        await query.edit_message_text("Erro: Cliente não encontrado. Por favor, inicie a conversa novamente.")
        return ConversationHandler.END

    async with httpx.AsyncClient() as client:
        cart_data = {"product_id": product_id, "quantity": quantity}
        response = await client.post(f"{BASE_API_URL}/cart/add/{client_id}/", json=cart_data)

    if response.status_code == 201:
        cart_info = response.json()
        await query.edit_message_text(
            f"Produto adicionado ao carrinho com sucesso!\n"
            f"Produto ID: {cart_info['product_id']}\n"
            f"Quantidade: {cart_info['quantity']}"
        )
    else:
        logger.error(f"Erro ao adicionar produto ao carrinho: {response.status_code} - {response.text}")
        await query.edit_message_text(f"Erro ao adicionar produto ao carrinho: {response.text}")

    return VIEW_CART


async def view_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Exibe os itens no carrinho."""
    query = update.callback_query
    await query.answer()

    # Verifica se o client_id está no contexto do usuário
    client_id = context.user_data.get('client_id')
    if not client_id:
        await query.edit_message_text("Erro: Cliente não encontrado. Por favor, inicie a conversa novamente.")
        return ConversationHandler.END

    try:
        # Faz a requisição para obter os itens do carrinho
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_API_URL}/cart/{client_id}/items/")

        if response.status_code != 200:
            await query.edit_message_text(f"Erro ao carregar carrinho: {response.json().get('error', response.text)}")
            return VIEW_CART

        cart_data = response.json()
        cart_items = cart_data.get('items', [])  # Garante que itens sejam extraídos, mesmo se vazio
    except Exception as e:
        await query.edit_message_text(f"Erro ao conectar ao servidor: {str(e)}")
        return VIEW_CART

    # Cria o teclado para exibir os itens no carrinho
    keyboard = []
    for item in cart_items:
        product_name = item.get('product', {}).get('name', 'Produto desconhecido')
        product_quantity = item.get('quantity', 0)
        cart_item_id = item.get('id', '0')

        keyboard.append([
            InlineKeyboardButton(f"{product_name} - {product_quantity}", callback_data="noop"),
            InlineKeyboardButton("+", callback_data=f"{INCREMENT}:{cart_item_id}"),
            InlineKeyboardButton("-", callback_data=f"{DECREMENT}:{cart_item_id}"),
        ])

    # Adiciona o botão para finalizar o pedido
    keyboard.append([InlineKeyboardButton("Finalizar Pedido", callback_data=str(CONFIRM))])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Exibe os itens do carrinho no Telegram
    await query.edit_message_text("Seu carrinho:", reply_markup=reply_markup)
    return VIEW_CART


async def update_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    action, item_id = query.data.split(":")
    action_type = "increase" if int(action) == INCREMENT else "decrease"

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_API_URL}/cart/update/{item_id}/", json={"action": action_type})
        if response.status_code != 200:
            await query.edit_message_text(f"Erro ao atualizar o item no carrinho: {response.text}")
            return await view_cart(update, context)

    return await view_cart(update, context)


async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    # Verifica se o client_id já está salvo
    client_id = context.user_data.get("client_id")
    if not client_id:
        await query.edit_message_text("Erro: Cliente não encontrado. Inicie o bot novamente.")
        return ConversationHandler.END

    # Solicita os dados do usuário para completar o pedido
    await query.edit_message_text("Por favor, envie seu nome:")
    return COLLECT_NAME


async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Agora, informe seu número de telefone:")
    return COLLECT_PHONE


async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["phone_number"] = update.message.text
    await update.message.reply_text("Informe a cidade:")
    return COLLECT_CITY


async def collect_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["city"] = update.message.text
    await update.message.reply_text("Informe o endereço completo:")
    return COLLECT_ADDRESS


async def collect_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["address"] = update.message.text
    client_id = context.user_data.get("client_id")

    async with httpx.AsyncClient() as client:
        # Finaliza o pedido usando client_id
        await client.post(f"{BASE_API_URL}/cart/checkout/{client_id}/", json={"address": context.user_data["address"]})

    await update.message.reply_text("Pedido finalizado com sucesso!")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("7202444496:AAG8ZSQw1S-nXsbHsnxX4h_lGB3XaJ6QzuI").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            VIEW_CATEGORIES: [
                CallbackQueryHandler(show_products, pattern=f"^{CATEGORY}:"),
                CallbackQueryHandler(view_cart, pattern="^view_cart$"), 
                CallbackQueryHandler(start, pattern="^view_categories$"),  # Exibe as categorias
            ],
            VIEW_PRODUCTS: [CallbackQueryHandler(add_product_to_cart, pattern=f"^{PRODUCT}:")],
            VIEW_CART: [
                CallbackQueryHandler(view_cart, pattern="^cart$"),
                CallbackQueryHandler(update_cart, pattern=f"^(increment|decrement):"),
            ],
            CONFIRM_ORDER: [CallbackQueryHandler(finalize_order, pattern="^confirm_order$")],
            COLLECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_name)],
            COLLECT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_phone)],
            COLLECT_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_city)],
            COLLECT_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_address)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
