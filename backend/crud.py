from typing import List, Optional
from backend.models import Item

# In-memory "database"
_items_db: List[Item] = []


def get_items() -> List[Item]:
    return _items_db


def get_item(item_id: int) -> Optional[Item]:
    for item in _items_db:
        if item.id == item_id:
            return item
    return None


def create_item(item: Item) -> Item:
    _items_db.append(item)
    return item


def update_item(item_id: int, new_item: Item) -> Optional[Item]:
    for idx, item in enumerate(_items_db):
        if item.id == item_id:
            _items_db[idx] = new_item
            return new_item
    return None


def delete_item(item_id: int) -> bool:
    for idx, item in enumerate(_items_db):
        if item.id == item_id:
            del _items_db[idx]
            return True
    return False
