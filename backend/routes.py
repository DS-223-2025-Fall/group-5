from typing import List

from fastapi import APIRouter, HTTPException

from backend.models import Item
from backend import crud  # import the whole module

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=List[Item])
def list_items():
    return crud.get_items()


@router.post("/", response_model=Item)
def create_item(item: Item):
    # simple check to avoid duplicate IDs
    if crud.get_item(item.id):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    return crud.create_item(item)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, new_item: Item):
    updated = crud.update_item(item_id, new_item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.delete("/{item_id}")
def delete_item(item_id: int):
    deleted = crud.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
