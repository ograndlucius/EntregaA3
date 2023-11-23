from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from pydantic import BaseModel

Base = declarative_base()

class ItemBase(BaseModel):
    nome: str
    descricao: str
    estoque: int
    preco: float

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

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

class UsuarioBase(BaseModel):
    nome: str
    email: str
    senha: str
    is_admin: bool

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    is_admin = Column(Boolean)

    # Adicionando relação com pedidos
    pedidos = relationship("PedidoDB", back_populates="usuario", primaryjoin="UsuarioDB.id == PedidoDB.usuario_id")

    @classmethod
    def create(cls, db: Session, usuario_create: UsuarioCreate):
        usuario = cls(**usuario_create.dict())
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 10):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def get_by_id(cls, db: Session, usuario_id: int):
        return db.query(cls).filter(cls.id == usuario_id).first()

    @classmethod
    def update(cls, db: Session, usuario_id: int, usuario_update: UsuarioCreate):
        usuario = cls.get_by_id(db, usuario_id)
        if usuario:
            for key, value in usuario_update.dict().items():
                setattr(usuario, key, value)
            db.commit()
            db.refresh(usuario)
        return usuario

    @classmethod
    def delete(cls, db: Session, usuario_id: int):
        usuario = cls.get_by_id(db, usuario_id)
        if usuario:
            db.delete(usuario)
            db.commit()
        return usuario
    
class PedidoResponse(BaseModel):
    id: int
    item_id: int
    quantidade: int
    usuario_id: int

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    item_id: int
    quantidade: int

class PedidoDB(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    quantidade = Column(Integer)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Adicionando relação com usuários
    usuario = relationship("UsuarioDB", back_populates="pedidos", primaryjoin="UsuarioDB.id == PedidoDB.usuario_id")

