from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- SCHEMAS DE USUÁRIO ---
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    perfil: Optional[str] = "vendedor"

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True

# --- SCHEMAS DE LOGIN ---
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    perfil: Optional[str] = None

# --- SCHEMAS DE CLIENTE ---
class ClienteBase(BaseModel):
    nome_empresa: str
    contato_responsavel: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    usuario_id: Optional[int] = None
    criado_em: datetime

    class Config:
        from_attributes = True

# --- SCHEMAS DE OPORTUNIDADE (KANBAN) ---
class OportunidadeBase(BaseModel):
    titulo: str
    valor: Optional[float] = 0.0
    estagio: Optional[str] = "Novo Contato" # Novo Contato, Em Negociação, Proposta Enviada, Fechado / Ganho, Perdido
    cliente_id: int

class OportunidadeCreate(OportunidadeBase):
    pass

class OportunidadeUpdate(BaseModel):
    titulo: Optional[str] = None
    valor: Optional[float] = None
    estagio: Optional[str] = None

class OportunidadeResponse(OportunidadeBase):
    id: int
    usuario_id: int
    atualizado_em: datetime

    class Config:
        from_attributes = True