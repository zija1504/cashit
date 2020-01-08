from typing import Dict, List, TextIO, Tuple, DefaultDict
import re
from collections import defaultdict
from .db import add_item_to_database


def get_date(temp_list: List[str]) -> str:
    date_re = re.compile(r"(^\d{4}-\d{2}-\d{2}$)")
    _date = temp_list.pop(0)
    _date = date_re.search(_date)
    if _date:
        return _date.group(0)
    else:
        raise Exception("No date format in first line of file")


def match_item_name_and_price(temporary_list: List[str]) -> DefaultDict[str, float]:
    item_name_re = re.compile(r"(^[a-żA-Ż\s]+)(?:)")  # like ser żółty
    item_price_re = re.compile(r"(\d*\.\d*)")  # cena
    items: DefaultDict[str, float] = defaultdict(float)
    for item in temporary_list:
        try:
            item_name = item_name_re.search(item).group(0)
            item_price = float(item_price_re.search(item).group(0))
            items[item_name] += item_price
        except AttributeError as e:
            print(e)
            raise e
    return items


def pre_processing(temporary_list: List[str]) -> List[Dict]:
    _date = get_date(temporary_list)
    temporary_list = [item.strip().replace(",", ".") for item in temporary_list]
    items = match_item_name_and_price(temporary_list)
    # dodaje date i kategorie ogólne
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


def postprocessing(database, temporary_list: List[Dict]):
    for data_dict in temporary_list:
        add_item_to_database(database, **data_dict)
