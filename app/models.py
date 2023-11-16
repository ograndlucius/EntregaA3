# app/models.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)  # Alterado para 'descricao' (não é uma palavra reservada)
    estoque = Column(Integer)

    @classmethod
    def create(cls, db, nome, descricao, estoque):  # Alterado para 'descricao' aqui também
        item = cls(nome=nome, descricao=descricao, estoque=estoque)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    
    @classmethod
    def get_all(cls, db, skip=0, limit=10):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db, item_id):
        return db.query(cls).filter(cls.id == item_id).first()

    @classmethod
    def update(cls, db, item_id, Nome, Desc, Estoque):
        item = cls.get_by_id(db, item_id)
        if item:
            item.Nome = Nome  # Alteração aqui
            item.Desc = Desc  # Alteração aqui
            item.Estoque = Estoque  # Alteração aqui
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
