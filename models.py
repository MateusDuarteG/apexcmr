from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(String, default="vendedor") # "admin" ou "vendedor"
    criado_em = Column(DateTime, default=datetime.utcnow)

    clientes = relationship("ClienteModel", back_populates="dono")
    oportunidades = relationship("OportunidadeModel", back_populates="responsavel")

class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome_empresa = Column(String, nullable=False)
    contato_responsavel = Column(String)
    email = Column(String)
    telefone = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    criado_em = Column(DateTime, default=datetime.utcnow)

    dono = relationship("UsuarioModel", back_populates="clientes")
    oportunidades = relationship("OportunidadeModel", back_populates="cliente")

class OportunidadeModel(Base):
    __tablename__ = "oportunidades"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    titulo = Column(String, nullable=False)
    valor = Column(Float, default=0.0)
    estagio = Column(String, default="Novo Contato") # Novo Contato, Em Negociação, Proposta Enviada, Fechado / Ganho, Perdido
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cliente = relationship("ClienteModel", back_populates="oportunidades")
    responsavel = relationship("UsuarioModel", back_populates="oportunidades")