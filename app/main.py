# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, database
from pydantic import BaseModel


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# Modelo Pydantic para representar a resposta da criação de um item
class ItemCreate(BaseModel):
    nome: str
    descricao: str
    estoque: int
    preco: float  # Adicionado o campo "preco"

# Função de dependência para obter uma sessão do banco de dados.
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para popular o banco de dados com dados de exemplo.
def seed_data(db: Session):
    db.query(models.Item).delete()
    products = [
        {'nome': "Nike Air", "descricao": "Sapato clássico e estiloso.", "estoque": 10, "preco": 499.99},
        {'nome': "Nike Air Max", "descricao": "Conforto e tecnologia para atletas.", "estoque": 15, "preco": 699.99},
        {'nome': "Nike Pine Green", "descricao": "Design moderno em verde.", "estoque": 8, "preco": 799.99},
        {'nome': "Nike Air Jordan", "descricao": "Estilo lendário do basquete.", "estoque": 12, "preco": 899.99},
        {'nome': "Nike Cactus", "descricao": "Toque de ousadia e estilo.", "estoque": 7, "preco": 1299.99},
        {'nome': "Nike Booster", "descricao": "Eleva seu estilo a outro nível.", "estoque": 10, "preco": 1199.99},
        {'nome': "Nike Yeezy", "descricao": "Design único e moderno.", "estoque": 20, "preco": 2499.99},
        {'nome': "Nike Downshifter", "descricao": "Conforto para o dia a dia.", "estoque": 18, "preco": 299.99},
        {'nome': "Nike Revolution", "descricao": "Performance e estilo em um só.", "estoque": 14, "preco": 449.99},
        {'nome': "Nike Flex", "descricao": "Flexibilidade para seus pés.", "estoque": 6, "preco": 349.99},
    ]

    for product in products:
        # Adição da chamada da função models.Item.create no loop for
        item = models.Item.create(db, product["nome"], product["descricao"], product["estoque"], product["preco"])
        print(f"Item criado: {item}")

## ROTAS ##
# Rota para criar um novo item
@app.post("/estoque/adicionar/", response_model=ItemCreate)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Retorno dos modelos reais (models.Item) nas respostas das rotas
    return models.Item.create(db, item.nome, item.descricao, item.estoque, item.preco)

# Rota para obter todos os itens
@app.get("/estoque/", response_model_exclude_unset=True)
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Retorno dos modelos reais (models.Item) nas respostas das rotas
    return models.Item.get_all(db, skip=skip, limit=limit)

# Rota para obter um item por ID
@app.get("/estoque/{item_id}", response_model_exclude_unset=True)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = models.Item.get_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return item

# Rota para atualizar um item por ID
@app.put("/update/{item_id}", response_model=ItemCreate)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    updated_item = models.Item.update(db, item_id, item.nome, item.descricao, item.estoque, item.preco)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return updated_item

# Rota para excluir um item por ID
@app.delete("/estoque/remove/{item_id}", response_model_exclude_unset=True)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted_item = models.Item.delete(db, item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return JSONResponse(content={"message": "Item excluído."})

# Endpoint para popular o banco de dados com dados de exemplo.
@app.post("/estoque/seed-data/", response_model=dict)
def seed_data_endpoint(db: Session = Depends(get_db)):
    seed_data(db)
    return {"message": "Dados de exemplo adicionados ao banco de dados."}