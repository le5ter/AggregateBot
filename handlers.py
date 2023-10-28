from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from database import get_collection

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Тест")


@router.message()
async def message_handler(msg: Message):
    collection = get_collection()
    cursor = collection.find({})
    i = 0
    for document in cursor:
        if i < 10:
            await msg.answer(f"{document}")
            i += 1
        else:
            break
