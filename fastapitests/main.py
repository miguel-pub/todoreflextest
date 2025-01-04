from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool = False

items = []


@app.get("/")
def root():
    return {"Hello": "World"}

#returns list of items starting at 0, stopping at limit
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10) -> list[Item]:
    return items[0:limit]

# posts to the list and appends to the end
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

#returns item at given itemid, which is index
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
    