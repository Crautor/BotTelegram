import logging
import httpx
import re
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

COLLECT_PHONE, COLLECT_ADDRESS, COLLECT_CITY = range(3)

# Base API URL
BASE_API_URL = "http://back:3001/api"

# Phone validation function
def is_valid_phone(phone: str) -> bool:
    """Validates if the phone number is in a correct format."""
    pattern = re.compile(r"^\+?\d{10,15}$")
    return bool(pattern.match(phone))

# Get or create client in the database
async def get_or_create_client(telegram_user_id: int, user_name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Retrieve or create a client in the database."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_API_URL}/client/{telegram_user_id}/")
            if response.status_code == 200:
                context.user_data["client_id"] = response.json().get("id")
                logger.info(f"Cliente encontrado. Client ID: {context.user_data['client_id']}")
                return True

            if response.status_code == 404:  # Client does not exist
                client_data = {"telegram_user_id": telegram_user_id, "name": user_name}
                response = await client.post(f"{BASE_API_URL}/client/create/", json=client_data)
                if response.status_code == 201:
                    context.user_data["client_id"] = response.json().get("id")
                    logger.info(f"Cliente criado com sucesso. Client ID: {context.user_data['client_id']}")
                    return True
                else:
                    logger.error(f"Falha ao criar cliente: {response.status_code} - {response.text}")
                    await context.bot.send_message(telegram_user_id, "Erro ao criar cliente. Tente novamente mais tarde.")
                    return False
            else:
                logger.error(f"Erro ao verificar cliente: {response.status_code} - {response.text}")
                await context.bot.send_message(telegram_user_id, "Erro ao verificar cliente. Tente novamente mais tarde.")
                return False
        except httpx.RequestError as e:
            logger.error(f"Erro de requisição: {e}")
            await context.bot.send_message(telegram_user_id, "Erro ao conectar ao servidor. Tente novamente mais tarde.")
            return False

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the bot and show the main menu."""
    user = update.message.from_user
    telegram_user_id = user.id
    logger.info(f"User {user.first_name} started the conversation with ID {telegram_user_id}.")

    if "client_id" not in context.user_data:
        if not await get_or_create_client(telegram_user_id, user.first_name, context):
            return ConversationHandler.END

    # Show initial menu
    keyboard = [
        [InlineKeyboardButton("Ver Categorias", callback_data="view_categories")],
        [InlineKeyboardButton("Ver Carrinho", callback_data="view_cart")],
        [InlineKeyboardButton("Finalizar Pedido", callback_data="confirm_order")],
        [InlineKeyboardButton("SOS - Suporte", callback_data="sos")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bem-vindo! Escolha uma opção:", reply_markup=reply_markup)
    return VIEW_CATEGORIES


async def send_error_message(telegram_user_id: int, message: str, context: ContextTypes.DEFAULT_TYPE):
    """Helper function to send error messages to users."""
    logger.error(f"Error message for user {telegram_user_id}: {message}")
    await context.bot.send_message(telegram_user_id, message)

async def sos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Acionar a lógica de SOS para suporte."""
    user_id = update.callback_query.from_user.id

    # Verifica se o usuário está no meio de um processo de coleta de dados
    if "collecting_data" in context.user_data and context.user_data["collecting_data"]:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text("Você está no meio de um processo. Por favor, finalize antes de solicitar suporte.")
        return

    # Marca que o usuário iniciou um fluxo SOS
    context.user_data["last_sos_user_id"] = user_id  # Salva o Telegram ID no contexto
    logger.info(f"Solicitação de SOS recebida de {update.callback_query.from_user.first_name} ({user_id})")
    
    # Mensagem inicial com botão de cancelamento para o usuário solicitante
    keyboard = [
        [InlineKeyboardButton("Cancelar Atendimento", callback_data="cancel_sos")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(
        "Você acionou o suporte! Nossa equipe está sendo notificada e em breve você receberá um atendimento. "
        "Enquanto isso, se precisar de algo urgente, por favor, nos informe!",
        reply_markup=reply_markup
    )

    # ID do administrador que será notificado
    admin_chat_id = 1938793005

    # Notificar o administrador
    await context.bot.send_message(
        admin_chat_id,
        f"🚨 Novo pedido de suporte!\n\n"
        f"Usuário: {update.callback_query.from_user.first_name} ({user_id})\n"
        f"Telegram ID: {user_id}\n"
        f"Mensagem: SOS"
    )

    # Mensagem de retorno para o usuário que solicitou o suporte
    await context.bot.send_message(
        chat_id=user_id,
        text="Sua solicitação de suporte foi recebida com sucesso! Um membro da equipe irá entrar em contato com você em breve."
    )

# Capturar mensagens do cliente e encaminhar ao último administrador
DEFAULT_ADMIN_ID = 1938793005


# Mostrar categorias
async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Exibe as categorias de produtos disponíveis."""
    query = update.callback_query
    await query.answer()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_API_URL}/category/")
            if response.status_code == 200:
                categories = response.json()
            else:
                await query.edit_message_text(f"Erro ao carregar categorias: {response.text}")
                return VIEW_CATEGORIES
    except httpx.RequestError as e:
        logger.error(f"Erro de requisição ao buscar categorias: {e}")
        await query.edit_message_text("Erro ao buscar categorias. Tente novamente mais tarde.")
        return VIEW_CATEGORIES

    keyboard = [
        [InlineKeyboardButton(category['name'], callback_data=f"category:{category['id']}")]
        for category in categories
    ]
    keyboard.append([InlineKeyboardButton("Voltar", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Escolha uma categoria:", reply_markup=reply_markup)
    return VIEW_CATEGORIES

async def cancel_sos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Permite que o administrador cancele a solicitação de SOS de um usuário."""
    admin_id = update.message.from_user.id
    allowed_admins = [1938793005]  # IDs dos administradores permitidos

    if admin_id not in allowed_admins:
        await update.message.reply_text("Você não tem permissão para usar este comando.")
        return

    # Obter os argumentos do comando
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Uso: /cancelar_sos <telegram_id>")
        return

    try:
        telegram_id = int(args[0])  # Primeiro argumento é o Telegram ID do usuário
    except ValueError:
        await update.message.reply_text("Erro: O Telegram ID deve ser numérico.")
        return

    # Cancelar o atendimento do SOS
    if "last_sos_user_id" in context.user_data and context.user_data["last_sos_user_id"] == telegram_id:
        # Limpar dados do usuário
        del context.user_data["last_sos_user_id"]

        await update.message.reply_text(f"O atendimento de SOS para o usuário {telegram_id} foi cancelado.")

        # Enviar uma mensagem para o usuário, informando o cancelamento
        try:
            await context.bot.send_message(telegram_id, "Seu pedido de suporte foi cancelado pelo administrador.")
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem ao usuário {telegram_id}: {e}")
            await update.message.reply_text("Erro ao tentar notificar o usuário.")
    else:
        await update.message.reply_text("Nenhuma solicitação de SOS ativa encontrada para esse usuário.")


# Show products from category
async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Exibe os produtos de uma categoria com imagens e botões inline."""
    query = update.callback_query
    await query.answer()

    category_id = query.data.split(":")[1]
    logger.info(f"User selected category ID: {category_id}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_API_URL}/product/category/{category_id}")
            if response.status_code == 200:
                products = response.json()
            else:
                await query.edit_message_text(f"Erro ao carregar produtos: {response.text}")
                return VIEW_CATEGORIES
    except httpx.RequestError as e:
        logger.error(f"Request error while fetching products: {e}")
        await query.edit_message_text("Erro ao buscar produtos. Tente novamente mais tarde.")
        return VIEW_CATEGORIES

    if products:
        # Envia uma mensagem com a foto e os botões para cada produto
        for prod in products:
            photo_url = prod.get("photo_url")
            product_name = prod.get("name")
            product_price = prod.get("price")
            product_id = prod.get("id")

            # Certifique-se de que product_price é numérico antes de formatar
            try:
                product_price = float(product_price)
            except (ValueError, TypeError):
                product_price = 0.0  # Defina um valor padrão ou trate o erro conforme necessário

            keyboard = [
                [InlineKeyboardButton(f"Selecionar {product_name} - R${product_price:.2f}", callback_data=f"product:{product_id}")]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            # Verifica se o produto tem uma URL de imagem válida
            if photo_url:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=photo_url,
                    caption=f"**{product_name}**\nPreço: R${product_price:.2f}",
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )
            else:
                # Caso não tenha imagem, envia somente a descrição
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"**{product_name}**\nPreço: R${product_price:.2f}",
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )

        # Adiciona o botão de voltar ao final
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Clique no botão abaixo para voltar.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Voltar", callback_data="view_categories")]])
        )
    else:
        await query.edit_message_text("Nenhum produto encontrado para esta categoria.")

    return VIEW_PRODUCTS


# Add product to cart
async def add_product_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Adiciona um produto ao carrinho.""" 
    query = update.callback_query
    await query.answer()

    product_id = query.data.split(":")[1]
    quantity = 1

    client_id = context.user_data.get('client_id')
    if not client_id:
        await query.edit_message_text("Erro: Cliente não encontrado. Por favor, inicie a conversa novamente.")
        return ConversationHandler.END

    try:
        async with httpx.AsyncClient() as client:
            cart_data = {"product_id": product_id, "quantity": quantity}
            response = await client.post(f"{BASE_API_URL}/cart/add/{client_id}/", json=cart_data)

            if response.status_code == 201:
                cart_info = response.json()
                # Monta a mensagem de sucesso com os detalhes do produto
                message_text = (
                    f"✅ Produto adicionado ao carrinho com sucesso!\n\n"
                    f"**Produto:** {cart_info.get('product_name', 'ID: ' + str(cart_info['product_id']))}\n"
                    f"**Quantidade:** {cart_info['quantity']}\n"
                    f"**Preço:** R${cart_info.get('price', 0.0):.2f}\n"
                    f"**Subtotal:** R${cart_info.get('subtotal', 0.0):.2f}"
                )
                await query.edit_message_text(message_text, parse_mode="Markdown")
            else:
                # Mostra mensagem de erro com a resposta da API
                await query.edit_message_text(
                    f"⚠️ Erro ao adicionar produto ao carrinho:\n{response.json().get('detail', 'Erro desconhecido.')}"
                )
    except httpx.RequestError as e:
        logger.error(f"Erro ao fazer requisição HTTP: {e}")
        await query.edit_message_text("❌ Erro ao adicionar produto ao carrinho. Tente novamente mais tarde.")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        await query.edit_message_text("❌ Ocorreu um erro inesperado. Tente novamente mais tarde.")

    return VIEW_CART


async def view_cart(update, context):
    """Exibe os itens no carrinho do usuário."""
    query = update.callback_query
    await query.answer()

    client_id = context.user_data.get("client_id")
    if not client_id:
        await query.edit_message_text("❌ Erro: Cliente não encontrado. Por favor, inicie a conversa novamente.")
        return ConversationHandler.END

    try:
        async with httpx.AsyncClient() as client:
            # Solicitação para obter os itens do carrinho
            response = await client.get(f"{BASE_API_URL}/cart/{client_id}/items/")
            
            if response.status_code == 200:
                cart_data = response.json()
                
                if cart_data.get("items"):
                    items_text = "\n".join(
                        [
                            f"**{item['product_name']}**\n"
                            f"Quantidade: {item['quantity']}\n"
                            f"Preço unitário: R${float(item['product_price']):.2f}\n"
                            f"Subtotal: R${float(item['product_price']) * item['quantity']:.2f}\n"
                            for item in cart_data["items"]
                        ]
                    )
                    total_price = sum(
                        float(item["product_price"]) * item["quantity"]
                        for item in cart_data["items"]
                    )
                    
                    cart_message = (
                        f"🛒 **Itens no carrinho:**\n\n{items_text}\n"
                        f"**Total:** R${total_price:.2f}"
                    )
                    await query.edit_message_text(cart_message, parse_mode="Markdown")
                else:
                    await query.edit_message_text("🛒 Seu carrinho está vazio.")
            else:
                error_message = response.json().get("detail", "Erro desconhecido.")
                await query.edit_message_text(f"⚠️ Erro ao carregar o carrinho:\n{error_message}")
    except httpx.RequestError as e:
        logger.error(f"Erro de requisição HTTP ao acessar o carrinho: {e}")
        await query.edit_message_text("❌ Erro ao acessar o carrinho. Tente novamente mais tarde.")
    except Exception as e:
        logger.error(f"Erro inesperado ao acessar o carrinho: {e}")
        await query.edit_message_text("❌ Ocorreu um erro inesperado. Tente novamente mais tarde.")

    
    
    return VIEW_CART

# Finalize order
async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia o processo de coleta de informações para finalizar o pedido."""
    # Marca que o usuário está no meio de um processo de coleta de dados
    context.user_data["collecting_data"] = True

    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Por favor, informe seu número de telefone.")
    return COLLECT_PHONE

# Função para responder ao cliente
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Permite ao administrador responder diretamente ao usuário."""
    admin_id = update.message.from_user.id
    allowed_admins = [1938793005]  # IDs dos administradores permitidos
    
    if admin_id not in allowed_admins:
        await update.message.reply_text("Você não tem permissão para usar este comando.")
        return

    # Obter argumentos do comando
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Uso: /responder <telegram_id> <mensagem>")
        return

    # Extrair o Telegram ID do usuário e a mensagem
    try:
        telegram_id = int(args[0])  # Primeiro argumento é o Telegram ID
        message = " ".join(args[1:])  # Restante é a mensagem
    except ValueError:
        await update.message.reply_text("Erro: O Telegram ID deve ser numérico.")
        return

    try:
        # Enviar mensagem para o usuário
        await context.bot.send_message(chat_id=telegram_id, text=f"Mensagem do Suporte:\n\n{message}")
        await update.message.reply_text("Mensagem enviada com sucesso!")
        
        # Registrar o último administrador que respondeu ao cliente
        context.user_data["last_admin_id"] = admin_id
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem ao usuário {telegram_id}: {e}")
        await update.message.reply_text("Erro ao enviar a mensagem. Verifique o Telegram ID.")


async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Coleta o número de telefone do cliente."""
    phone_number = update.message.text.strip()

    # Validação simples do número de telefone
    if not is_valid_phone(phone_number):
        await update.message.reply_text("Número de telefone inválido. Por favor, informe um número válido.")
        return COLLECT_PHONE

    # Armazenando o número de telefone no contexto
    context.user_data["phone"] = phone_number

    # Continuar para o próximo passo
    await update.message.reply_text("Agora, por favor, informe seu endereço (endereço completo).")
    return COLLECT_ADDRESS

# Função para coletar o endereço
async def collect_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Coleta o endereço do cliente."""
    address = update.message.text.strip()

    # Armazenando o endereço no contexto
    context.user_data["address"] = address

    # Continuar para coletar a cidade
    await update.message.reply_text("Agora, por favor, informe sua cidade.")
    return COLLECT_CITY

# Função para coletar a cidade
async def collect_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Coleta a cidade do cliente."""
    city = update.message.text.strip()

    # Armazenando a cidade no contexto
    context.user_data["city"] = city

    # Agora que temos todos os dados, podemos criar a ordem
    await create_order(update, context)

    # Limpa o estado de coleta de dados
    context.user_data["collecting_data"] = False

    return ConversationHandler.END

# Função para criar a ordem no banco de dados
async def create_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cria a ordem no banco de dados com os dados coletados."""
    phone = context.user_data.get("phone")
    address = context.user_data.get("address")
    city = context.user_data.get("city")

    # Aqui você pode fazer uma solicitação HTTP para criar a ordem no seu banco de dados
    async with httpx.AsyncClient() as client:
        order_data = {
            "phone": phone,
            "address": address,
            "city": city,
            # Adicione outros campos necessários para a criação da ordem
        }

        try:
            response = await client.post(f"{BASE_API_URL}/order/create/", json=order_data)

            if response.status_code == 201:
                await update.message.reply_text("Seu pedido foi criado com sucesso!")
            else:
                await update.message.reply_text("Houve um erro ao criar seu pedido. Tente novamente mais tarde.")
        except httpx.RequestError as e:
            logger.error(f"Erro de requisição ao criar pedido: {e}")
            await update.message.reply_text("Erro ao criar seu pedido. Tente novamente mais tarde.")

# Função para responder ao cliente
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Permite ao administrador responder diretamente ao usuário."""
    admin_id = update.message.from_user.id
    allowed_admins = [1938793005]  # IDs dos administradores permitidos
    
    if admin_id not in allowed_admins:
        await update.message.reply_text("Você não tem permissão para usar este comando.")
        return

    # Obter argumentos do comando
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Uso: /responder <telegram_id> <mensagem>")
        return

    # Extrair o Telegram ID do usuário e a mensagem
    try:
        telegram_id = int(args[0])  # Primeiro argumento é o Telegram ID
        message = " ".join(args[1:])  # Restante é a mensagem
    except ValueError:
        await update.message.reply_text("Erro: O Telegram ID deve ser numérico.")
        return

    try:
        # Enviar mensagem para o usuário
        await context.bot.send_message(chat_id=telegram_id, text=f"Mensagem do Suporte:\n\n{message}")
        await update.message.reply_text("Mensagem enviada com sucesso!")
        
        # Registrar o último administrador que respondeu ao cliente
        context.user_data["last_admin_id"] = admin_id
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem ao usuário {telegram_id}: {e}")
        await update.message.reply_text("Erro ao enviar a mensagem. Verifique o Telegram ID.")

# Função para encaminhar mensagens ao admin, se não estiver em coleta de dados
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Encaminha mensagens do cliente para o último administrador que respondeu."""
    
    # Verifica se o usuário está no processo de coleta de dados para pedido
    if context.user_data.get("collecting_data"):
        await update.message.reply_text("Estamos processando seu pedido, por favor aguarde.")
        return
    
    user = update.message.from_user
    message = update.message.text  # Captura o texto enviado pelo cliente
    
    # Recuperar o último admin que respondeu ou usar o padrão
    last_admin_id = context.user_data.get("last_admin_id", 1938793005)  # Substitua com seu ID de admin

    try:
        # Encaminhar a mensagem ao administrador
        await context.bot.send_message(
            chat_id=last_admin_id,
            text=f"📩 Resposta de {user.first_name} ({user.id}):\n\n{message}"
        )
        await update.message.reply_text("Sua mensagem foi enviada ao suporte com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao encaminhar mensagem do cliente {user.id} ao admin {last_admin_id}: {e}")
        await update.message.reply_text("Erro ao encaminhar a mensagem. Tente novamente mais tarde.")




# Main function to run the bot
def main():
    """Função principal para iniciar o bot."""
    application = Application.builder().token("7327581607:AAHG84Ie_4dR8LPSxkGP_ZAEZVZtD4NGYyw").build()

    # Registrando os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_categories, pattern="^view_categories$"))
    application.add_handler(CallbackQueryHandler(show_products, pattern="^category:\d+$"))
    application.add_handler(CallbackQueryHandler(add_product_to_cart, pattern="^product:\d+$"))
    application.add_handler(CallbackQueryHandler(finalize_order, pattern="^confirm_order$"))
    application.add_handler(CallbackQueryHandler(view_cart, pattern="^view_cart$"))
    application.add_handler(CallbackQueryHandler(sos, pattern="^sos$"))
    application.add_handler(CommandHandler("responder", responder))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    application.add_handler(CallbackQueryHandler(cancel_sos, pattern="^cancel_sos$"))
    
    conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(finalize_order, pattern="^confirm_order$")],
        states={
            COLLECT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_phone)],
            COLLECT_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_address)],
            COLLECT_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_city)],
        },
        fallbacks=[],
    )
    application.add_handler(conversation_handler)
 # Adicionando o handler de carrinho


    application.run_polling()

if __name__ == '__main__':
    main()
