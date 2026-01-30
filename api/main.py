import os
import django
from fastapi import FastAPI, HTTPException, Query
from api.schemas import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.database')
django.setup()

from api.models import Item

app = FastAPI(title="Key-Value API")

@app.get("/")
def root():
    return {"message": "Key-Value API"}

@app.post("/items/", response_model=ItemResponse)
def create_item(data: ItemCreate):
    if Item.objects.filter(key=data.key).exists():
        raise HTTPException(status_code=409, detail="key already exists")
    item = Item.objects.create(key=data.key, value=data.value)
    return ItemResponse(
        key=item.key,
        value=item.value,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )

@app.get("/items/{key}", response_model=ItemResponse)
def get_item(key: str):
    try:
        item = Item.objects.get(key=key)
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="item not found")
    return ItemResponse(
        key=item.key,
        value=item.value,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )

@app.put("/items/{key}", response_model=ItemResponse)
def update_item(key: str, data: ItemUpdate):
    try:
        item = Item.objects.get(key=key)
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="item not found")
    item.value = data.value
    item.save()
    return ItemResponse(
        key=item.key,
        value=item.value,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )

@app.delete("/items/{key}")
def delete_item(key: str):
    try:
        item = Item.objects.get(key=key)
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="item not found")
    item.delete()
    return {"message": "deleted"}

@app.get("/items/", response_model=ItemListResponse)
def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    total = Item.objects.count()
    start = (page - 1) * page_size
    end = start + page_size
    qs = Item.objects.all()[start:end]
    items = [
        ItemResponse(
            key=obj.key,
            value=obj.value,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
        for obj in qs
    ]
    return ItemListResponse(items=items, total=total, page=page, page_size=page_size)
