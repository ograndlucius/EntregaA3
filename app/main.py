# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, database
from pydantic import BaseModel

app = FastAPI()

# Modelo Pydantic para representar a resposta da criação de um item
class ItemCreate(BaseModel):
    nome: str
    descricao: str
    estoque: int

# Função de dependência para obter uma sessão do banco de dados.
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Função para popular o banco de dados com dados de exemplo.
def seed_data(db: Session):
    products = [
        {'nome': "Produto 1", "Desc": "Descrição do Produto 1", "Estoque": 50},
        {"Nome": "Produto 2", "Desc": "Descrição do Produto 2", "Estoque": 30},
        {"Nome": "Produto 3", "Desc": "Descrição do Produto 3", "Estoque": 20},
        {"Nome": "Produto 4", "Desc": "Descrição do Produto 4", "Estoque": 10},
        {"Nome": "Produto 5", "Desc": "Descrição do Produto 5", "Estoque": 40},
        {"Nome": "Produto 6", "Desc": "Descrição do Produto 6", "Estoque": 15},
        {"Nome": "Produto 7", "Desc": "Descrição do Produto 7", "Estoque": 25},
        {"Nome": "Produto 8", "Desc": "Descrição do Produto 8", "Estoque": 35},
        {"Nome": "Produto 9", "Desc": "Descrição do Produto 9", "Estoque": 45},
        {"Nome": "Produto 10", "Desc": "Descrição do Produto 10", "Estoque": 5},
    ]

## ROTAS ##
# Rota para criar um novo item
@app.post("/items/", response_model=ItemCreate)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return models.Item.create(db, item.nome, item.descricao, item.estoque)

# Rota para obter todos os itens
@app.get("/todositems/")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return models.Item.get_all(db, skip=skip, limit=limit)

# Rota para obter um item por ID
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = models.Item.get_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Rota para atualizar um item por ID
@app.put("/items/{item_id}", response_model=ItemCreate)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    updated_item = models.Item.update(db, item_id, item.name, item.description, item.stock_quantity)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

# Rota para excluir um item por ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted_item = models.Item.delete(db, item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(content={"message": "Item deleted"})

# Endpoint para popular o banco de dados com dados de exemplo.
@app.post("/seed-data/", response_model=dict)
def seed_data_endpoint(db: Session = Depends(get_db)):
    seed_data(db)
    return {"message": "Dados de exemplo adicionados ao banco de dados."}
