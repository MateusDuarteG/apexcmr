from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import models, schemas, auth
from database import engine, get_db

# Cria as tabelas no SQLite automaticamente ao iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM Backend API", version="1.0.0")

# Configuração de CORS para permitir requisições do Frontend (Live Server / HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/usuarios/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.UsuarioModel).filter(models.UsuarioModel.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado no sistema.")
    
    hashed_password = auth.gerar_hash_senha(usuario.senha)
    novo_usuario = models.UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hashed_password,
        perfil=usuario.perfil
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.UsuarioModel).filter(models.UsuarioModel.email == form_data.username).first()
    if not usuario or not auth.verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.criar_access_token(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/perfil/me", response_model=schemas.UsuarioResponse)
def ler_perfil_atual(usuario_atual: models.UsuarioModel = Depends(auth.obter_usuario_atual)):
    return usuario_atual

@app.post("/clientes/", response_model=schemas.ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(
    cliente: schemas.ClienteCreate, 
    db: Session = Depends(get_db), 
    usuario_atual: models.UsuarioModel = Depends(auth.obter_usuario_atual)
):
    novo_cliente = models.ClienteModel(**cliente.dict(), usuario_id=usuario_atual.id)
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@app.get("/clientes/", response_model=List[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db), usuario_atual: models.UsuarioModel = Depends(auth.obter_usuario_atual)):
    if usuario_atual.perfil == "admin":
        return db.query(models.ClienteModel).all()
    return db.query(models.ClienteModel).filter(models.ClienteModel.usuario_id == usuario_atual.id).all()

@app.post("/oportunidades/", response_model=schemas.OportunidadeResponse, status_code=status.HTTP_201_CREATED)
def criar_oportunidade(
    oportunidade: schemas.OportunidadeCreate, 
    db: Session = Depends(get_db), 
    usuario_atual: models.UsuarioModel = Depends(auth.obter_usuario_atual)
):
    cliente = db.query(models.ClienteModel).filter(models.ClienteModel.id == oportunidade.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    nova_op = models.OportunidadeModel(**oportunidade.dict(), usuario_id=usuario_atual.id)
    db.add(nova_op)
    db.commit()
    db.refresh(nova_op)
    return nova_op

@app.get("/oportunidades/", response_model=List[schemas.OportunidadeResponse])
def listar_oportunidades(db: Session = Depends(get_db), usuario_atual: models.UsuarioModel = Depends(auth.obter_usuario_atual)):
    if usuario_atual.perfil == "admin":
        return db.query(models.OportunidadeModel).all()
    return db.query(models.OportunidadeModel).filter(models.OportunidadeModel.usuario_id == usuario_atual.id).all()

@app.patch("/oportunidades/{oportunidade_id}", response_model=schemas.OportunidadeResponse)
def atualizar_estagio_oportunidade(
    oportunidade_id: int, 
    dados_atualizacao: schemas.OportunidadeUpdate, 
    db: Session = Depends(get_db), 
    usuario_atual: models.UsuarioModel = Depends(auth.obter_usuario_atual)
):
    op = db.query(models.OportunidadeModel).filter(models.OportunidadeModel.id == oportunidade_id).first()
    if not op:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada.")
    
    if usuario_atual.perfil != "admin" and op.usuario_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Acesso negado.")

    update_data = dados_atualizacao.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(op, key, value)

    db.commit()
    db.refresh(op)
    return op

@app.get("/usuarios/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db), 
    usuario_atual: models.UsuarioModel = Depends(auth.obter_administrador_atual)
):
    return db.query(models.UsuarioModel).all()