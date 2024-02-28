from sqlalchemy import create_engine, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (Column, Uuid, Datatime, func, String, DECIMAL,
                        Foreingkey, Boolean, integer)

motor = create_engine ("sqlite+pysqlite://banco_de_dados.sqlite",
                       echo=True)


class Base(DeclarativeBase):
    pass

class DataMixin():
    data_cadastro = Column(Datatime,
                           server_default=func.now(),
                           nullable=False)
    data_atualizacao = Column(Datatime,
                              onupdate=func.now(),
                              default=func.now(),
                              nullable=False)


class Categoria(Base, DataMixin):
    __tablename__ = "tbl_categorias"
    id = Column(Uuid(as_uuid=True),
                primary_key=True,
                default=Uuid.uuid4())
    nome = Column(String(256),
                  nullable=False)
    lista_de_produtos = relationship ("Produto", back_populates="Categoria",
                                      cascade="all, detele-orphan", lazy="selectin")


class Produto(Base):
    __tablename__ = "tbl_produtos"
    id = Column(Uuid(as_uuid=True),
                primary_key=True,
                default=Uuid.uuid4())
    nome = Column(String(256),
                  nullable=False)
    preco = Column (DECIMAL(10,2),
                    nullable=False,
                    default=0.00)
    estoque = Column (integer, default=0)
    ativo = Column(Boolean, default=True)
    categoria_id = Column(Uuid(as_uuid=True), Foreingkey("tbl_categorias.id"))

    categoria = relationship("Categoria", back_populates="lista_de_produtos")