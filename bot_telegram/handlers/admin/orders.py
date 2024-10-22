from aiogram.types import Message
from loader import dp, db
from handlers.user.menu import orders
from filters import IsAdmin

@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    # Buscar todos os pedidos no banco de dados
    orders = db.fetchall('SELECT * FROM orders')
    
    # Verificar se há pedidos
    if len(orders) == 0:
        await message.answer('Você não tem pedidos.')
    else:
        await order_answer(message, orders)

async def order_answer(message, orders):
    # Preparar a resposta com os pedidos
    res = ''
    for order in orders:
        res += f'Pedido <b>№{order[3]}</b>\n\n'

    # Enviar a mensagem com a lista de pedidos
    await message.answer(res)
