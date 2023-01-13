
import re
from aiogram.dispatcher.filters import Command
import app.keyboards.inline_keyboard as kb
from loader import dp, bot
from aiogram import types, Dispatcher
from app.services.application import ApplicationService
from dependency_injector.wiring import inject, Provide
from app.models.application import Application
from states.base import Admin
from aiogram.dispatcher import FSMContext
from logger import logger

from app.core.container import Container


@inject
async def admin(message: types.Message,
                application: ApplicationService = Provide[Container.application_service]):
    try:
        tickets = await application.applications_for(
            Application.RequestAnswered.admin)
        await kb.admin_btns_tickets(message=message, tickets=tickets)
    except:
        await message.answer('Новых обновлений нет')


@inject
async def characters_page_callback(call: types.CallbackQuery,
                                   application: ApplicationService = Provide[Container.application_service]):
    page = int(call.data.split('#')[1])
    tickets = await application.applications_for(
        Application.RequestAnswered.admin)
    await kb.admin_btns_tickets(call.message, tickets, page)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


async def comeback(query: types.CallbackQuery,
                   state: FSMContext):
    number = re.search(r'\А(.+?)(\n|$)', query.message.text).groups()
    user_id = int(re.search(r'(?<=12\)).*', query.message.text).group())
    logger.info(user_id)
    await state.update_data(number=int(number[0]), user_id=user_id)
    await query.message.answer('Ведите комментарий: ')
    await state.set_state(Admin.comment)


@inject
async def get_comment(message: types.Message, state: FSMContext,
                      application: ApplicationService = Provide[Container.application_service]):
    admin_data = await state.get_data()
    await bot.send_message(admin_data['user_id'], message.text)
    await application.delete(admin_data['number'])
    await state.finish()


def register_chat_handler(dp: Dispatcher):
    dp.register_message_handler(admin, Command('admin'))
    dp.register_message_handler(get_comment, state=Admin.comment)
    dp.register_callback_query_handler(comeback, text='comeback')
    dp.register_callback_query_handler(characters_page_callback, lambda call: call.data.split('#')[0]=='ticket')
    