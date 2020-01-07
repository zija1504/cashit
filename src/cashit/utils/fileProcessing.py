from typing import Dict, List, TextIO, Tuple, DefaultDict
import re
from collections import defaultdict
from .db import add_item_to_database


def pre_processing(temporary_list: List[str]) -> List[Dict]:
    _date = temporary_list.pop(0)
    temporary_list = [item.strip().replace(",", ".") for item in temporary_list]
    item_name_re = re.compile(r"(^[a-żA-Ż\s]*)(?:)")  # like ser żółty
    item_price_re = re.compile(r"(\d*\.\d*)")  # cena
    items: DefaultDict[str, float] = defaultdict(float)
    for item in temporary_list:
        try:
            item_name = item_name_re.search(item).group(0)
            item_price = float(item_price_re.search(item).group(0))
            items[item_name] += item_price
        except Exception as e:
            print(e)
    items_list = [
        dict(name=k, price=v, date=_date, category="ogólne") for k, v in items.items()
    ]
    return items_list


def edit_utils(temporaryList: List[Dict], items_to_edit: Dict, new_values: Dict):
    price = 0
    _date = temporaryList[0]["date"]
    for name in items_to_edit["name"]:
        for index, x in enumerate(temporaryList):
            if name == x["name"]:
                price += x["price"]
                temporaryList.pop(index)

    temporaryList.append(
        dict(
            name=new_values["name"],
            price=price,
            date=_date,
            category=new_values["category"],
        )
    )


def postprocessing(temporary_list: List[Dict]):
    for data_dict in temporary_list:
        add_item_to_database(**data_dict)
