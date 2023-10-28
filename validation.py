import json
import re
from json import JSONDecodeError


def is_valid_datetime_string(datetime_str):
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
    return re.match(pattern, datetime_str) is not None


def is_valid_message(message: str):

    if message.find("{") == -1 or message.find("}") == -1:
        return False
    else:
        try:
            data = json.loads(message)

            # Проверка на наличие всех обязательных полей
            if "dt_from" in data and "dt_upto" in data and "group_type" in data:
                # Проверка формата дат и типа группировки
                dt_from = data["dt_from"]
                dt_upto = data["dt_upto"]
                group_type = data["group_type"]

                valid_group_type_values = ["month", "day", "hour"]

                if is_valid_datetime_string(dt_from) and is_valid_datetime_string(
                        dt_upto) and group_type in valid_group_type_values:
                    return True
        except JSONDecodeError:
            return False
