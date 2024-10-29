from handlers.user.menu import questions
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from keyboards.default.markups import all_right_message, cancel_message, submit_markup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types.chat import ChatActions
from states import AnswerState
from loader import dp, db, bot
from filters import IsAdmin

question_cb = CallbackData('question', 'cid', 'action')


@dp.message_handler(IsAdmin(), text=questions)
async def process_questions(message: Message):

    # Indicar que o bot está digitando
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    # Buscar perguntas do banco de dados
    questions = db.fetchall('SELECT * FROM questions')

    if len(questions) == 0:
        await message.answer('Não há perguntas.')
    else:
        for cid, question in questions:
            # Criar um botão para responder à pergunta
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                'Responder', callback_data=question_cb.new(cid=cid, action='answer')))
            # Enviar a pergunta com o botão
            await message.answer(question, reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), question_cb.filter(action='answer'))
async def process_answer(query: CallbackQuery, callback_data: dict, state: FSMContext):
    # Armazenar o ID do usuário que fez a pergunta
    async with state.proxy() as data:
        data['cid'] = callback_data['cid']

    # Solicitar a resposta
    await query.message.answer('Escreva a resposta.', reply_markup=ReplyKeyboardRemove())
    # Mudar para o estado de responder
    await AnswerState.answer.set()


@dp.message_handler(IsAdmin(), state=AnswerState.answer)
async def process_submit(message: Message, state: FSMContext):
    # Armazenar a resposta fornecida pelo usuário
    async with state.proxy() as data:
        data['answer'] = message.text

    # Passar para o próximo estado e confirmar a resposta
    await AnswerState.next()
    await message.answer('Certifique-se de que a resposta está correta.', reply_markup=submit_markup())


@dp.message_handler(IsAdmin(), text=cancel_message, state=AnswerState.submit)
async def process_send_answer(message: Message, state: FSMContext):
    # Cancelar o envio da resposta
    await message.answer('Cancelado!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(IsAdmin(), text=all_right_message, state=AnswerState.submit)
async def process_send_answer(message: Message, state: FSMContext):
    # Enviar a resposta para o usuário
    async with state.proxy() as data:
        answer = data['answer']
        cid = data['cid']
        # Buscar a pergunta original
        question = db.fetchone(
            'SELECT question FROM questions WHERE cid=?', (cid,))[0]
        # Remover a pergunta do banco de dados
        db.query('DELETE FROM questions WHERE cid=?', (cid,))
        # Montar a mensagem com a pergunta e a resposta
        text = f'Pergunta: <b>{question}</b>\n\nResposta: <b>{answer}</b>'

        # Informar que a resposta foi enviada e enviar para o usuário
        await message.answer('Enviado!', reply_markup=ReplyKeyboardRemove())
        await bot.send_message(cid, text)

    # Finalizar o estado
    await state.finish()
