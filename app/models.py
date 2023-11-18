# app/models.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel

Base = declarative_base()

class Item(BaseModel):
    id: int
    nome: str
    descricao: str
    estoque: int
    preco: float

    class Config:
        orm_mode = True

class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    estoque = Column(Integer)
    preco = Column(Float)

    @classmethod
    def create(cls, db: Session, nome: str, descricao: str, estoque: int, preco: float):
        item = cls(nome=nome, descricao=descricao, estoque=estoque, preco=preco)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @classmethod
    def get_all(cls, db, skip=0, limit=100):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db, item_id):
        return db.query(cls).filter(cls.id == item_id).first()

    @classmethod
    def update(cls, db, item_id, nome, descricao, estoque, preco):
        item = cls.get_by_id(db, item_id)
        if item:
            item.nome = nome
            item.descricao = descricao
            item.estoque = estoque
            item.preco = preco
            db.commit()
            db.refresh(item)
        return item

    @classmethod
    def delete(cls, db, item_id):
        item = cls.get_by_id(db, item_id)
        if item:
            db.delete(item)
            db.commit()
        return item
