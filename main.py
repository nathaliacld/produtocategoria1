import uuid
from sqlalchemy import (Column, Uuid, DateTime, func, String, DECIMAL,
                        ForeignKey, Boolean, Integer)
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, relationship, Session

motor = create_engine("sqlite+pysqlite:///banco_de_dados.sqlite",
                      echo=True)


class Base(DeclarativeBase):
    pass


class DataMixin:
    data_cadastro = Column(DateTime,
                           server_default=func.now(),
                           nullable=False)
    data_atualizacao = Column(DateTime,
                              onupdate=func.now(),
                              default=func.now(),
                              nullable=False)


class Categoria(Base, DataMixin):
    __tablename__ = "tbl_categorias"
    id = Column(Uuid(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    nome = Column(String(256),
                  nullable=False)
    lista_de_produtos = relationship("Produto", back_populates="Categoria",
                                     cascade="all, delete-orphan", lazy="selectin")


class Produto(Base):
    __tablename__ = "tbl_produtos"
    id = Column(Uuid(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    nome = Column(String(256),
                  nullable=False)
    preco = Column(DECIMAL(10, 2),
                   nullable=False,
                   default=0.00)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    categoria_id = Column(Uuid(as_uuid=True), ForeignKey("tbl_categorias.id"))

    categoria = relationship("Categoria", back_populates="lista_de_produtos")

cat = Categoria()
cat.nome = "Bebidas"


prod = Produto()
prod.nome = 'Coca cola zero, 2L'
prod.ativo = True
prod.preco = 9.50
prod.estoque = 100
prod.categoria = cat

with Session(motor) as sessao:
     sessao.add(prod)
     sessao.commit()

with Session(motor) as sessao:
    categorias = sessao.execute(select(Categoria).where(Categoria.nome == 'Bebidas')).scalars()
    for categoria in categorias:
        print(f"A categoria {categoria.nome} tem {len(categoria.lista_de_produtos)} produtos")



