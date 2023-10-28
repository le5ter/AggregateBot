from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
from dateutil.relativedelta import relativedelta

from database import get_collection
import ast

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(f"Hello {msg.from_user.username}")


@router.message()
async def message_handler(msg: Message):
    collection = get_collection()

    # получаем данные из сообщения
    input_data = ast.literal_eval(msg.text)

    # Преобразовываем даты в объекты datetime
    dt_from = datetime.fromisoformat(input_data["dt_from"])
    dt_upto = datetime.fromisoformat(input_data["dt_upto"])

    # Определяем интервал времени для группировки
    if input_data["group_type"] == "hour":
        delta = relativedelta(hours=1)
    elif input_data["group_type"] == "day":
        delta = relativedelta(days=1)
    elif input_data["group_type"] == "month":
        delta = relativedelta(months=1)
    else:
        delta = relativedelta(hours=1)  # По умолчанию, если тип не распознан

    dataset = []
    labels = []

    current_date = dt_from
    while current_date <= dt_upto:
        next_date = current_date + delta

        # Выполняем агрегацию данных в MongoDB
        aggregation_pipeline = [
            {
                "$match": {
                    "dt": {
                        "$gte": current_date,
                        "$lt": next_date
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_salary": {"$sum": "$value"}
                }
            }
        ]

        result = list(collection.aggregate(aggregation_pipeline))

        # Добавляем результаты агрегации в массивы данных и меток
        if result:
            dataset.append(result[0]["total_salary"])
        else:
            dataset.append(0)

        labels.append(current_date.isoformat())

        current_date = next_date

    # Формируем ответ
    response = {
        "dataset": dataset,
        "labels": labels
    }

    await msg.answer(f'{response}')
