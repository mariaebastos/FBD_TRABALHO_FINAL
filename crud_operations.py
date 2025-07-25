from sqlalchemy.orm import Session
from datetime import date
from backend.models import Fabricante, Vacina, UnidadeSaude, Paciente, Aplicacao

# --- Funções CRUD para Fabricante ---
def get_fabricantes(db: Session, nome: str = None):
    query = db.query(Fabricante)
    if nome:
        query = query.filter(Fabricante.nome.ilike(f"%{nome}%"))
    return query.all()

def create_fabricante(db: Session, nome: str):
    db_fabricante = Fabricante(nome=nome)
    db.add(db_fabricante)
    db.commit()
    db.refresh(db_fabricante)
    return db_fabricante

def delete_fabricante(db: Session, fabricante_id: int):
    db_fabricante = db.query(Fabricante).filter(Fabricante.id == fabricante_id).first()
    if db_fabricante:
        db.delete(db_fabricante)
        db.commit()
    return db_fabricante

# --- Funções CRUD para Vacina ---
def get_vacinas(db: Session, nome: str = None, tipo: str = None, fabricante_nome: str = None):
    query = db.query(Vacina)
    if nome:
        query = query.filter(Vacina.nome.ilike(f"%{nome}%"))
    if tipo:
        query = query.filter(Vacina.tipo.ilike(f"%{tipo}%"))
    if fabricante_nome:
        query = query.join(Fabricante).filter(Fabricante.nome.ilike(f"%{fabricante_nome}%"))
    return query.all()

def get_vacina_by_id(db: Session, vacina_id: int):
    return db.query(Vacina).filter(Vacina.id == vacina_id).first()

def create_vacina(db: Session, nome: str, tipo: str, fabricante_id: int):
    db_vacina = Vacina(nome=nome, tipo=tipo, fabricante_id=fabricante_id)
    db.add(db_vacina)
    db.commit()
    db.refresh(db_vacina)
    return db_vacina

def update_vacina(db: Session, vacina_id: int, new_nome: str = None, new_tipo: str = None, new_fabricante_id: int = None):
    db_vacina = db.query(Vacina).filter(Vacina.id == vacina_id).first()
    if db_vacina:
        if new_nome: db_vacina.nome = new_nome
        if new_tipo: db_vacina.tipo = new_tipo
        if new_fabricante_id: db_vacina.fabricante_id = new_fabricante_id
        db.commit()
        db.refresh(db_vacina)
    return db_vacina

def delete_vacina(db: Session, vacina_id: int):
    db_vacina = db.query(Vacina).filter(Vacina.id == vacina_id).first()
    if db_vacina:
        db.delete(db_vacina)
        db.commit()
    return db_vacina

# --- Funções CRUD para UnidadeSaude ---
def get_unidades_saude(db: Session, nome: str = None, endereco: str = None):
    query = db.query(UnidadeSaude)
    if nome:
        query = query.filter(UnidadeSaude.nome.ilike(f"%{nome}%"))
    if endereco:
        query = query.filter(UnidadeSaude.endereco.ilike(f"%{endereco}%"))
    return query.all()

def get_unidade_saude_by_id(db: Session, unidade_id: int):
    return db.query(UnidadeSaude).filter(UnidadeSaude.id == unidade_id).first()

def create_unidade_saude(db: Session, nome: str, endereco: str):
    db_unidade = UnidadeSaude(nome=nome, endereco=endereco)
    db.add(db_unidade)
    db.commit()
    db.refresh(db_unidade)
    return db_unidade

def delete_unidade_saude(db: Session, unidade_id: int):
    db_unidade = db.query(UnidadeSaude).filter(UnidadeSaude.id == unidade_id).first()
    if db_unidade:
        db.delete(db_unidade)
        db.commit()
    return db_unidade

# --- Funções CRUD para Paciente ---
def get_pacientes(db: Session, nome: str = None, cpf: str = None):
    query = db.query(Paciente)
    if nome:
        query = query.filter(Paciente.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(Paciente.cpf == cpf)
    return query.all()

def get_paciente_by_id(db: Session, paciente_id: int):
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()

def create_paciente(db: Session, nome: str, data_nascimento: date, cpf: str):
    db_paciente = Paciente(nome=nome, data_nascimento=data_nascimento, cpf=cpf)
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def delete_paciente(db: Session, paciente_id: int):
    db_paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
    return db_paciente

# --- Funções CRUD para Aplicacao ---
def get_aplicacoes(db: Session, paciente_nome: str = None, vacina_nome: str = None, unidade_nome: str = None, data_aplicacao: date = None):
    query = db.query(Aplicacao).join(Paciente).join(Vacina).join(UnidadeSaude)
    if paciente_nome:
        query = query.filter(Paciente.nome.ilike(f"%{paciente_nome}%"))
    if vacina_nome:
        query = query.filter(Vacina.nome.ilike(f"%{vacina_nome}%"))
    if unidade_nome:
        query = query.filter(UnidadeSaude.nome.ilike(f"%{unidade_nome}%"))
    if data_aplicacao:
        query = query.filter(Aplicacao.data_aplicacao == data_aplicacao)
    return query.all()

def create_aplicacao(db: Session, paciente_id: int, vacina_id: int, unidade_id: int, data_aplicacao: date):
    db_aplicacao = Aplicacao(paciente_id=paciente_id, vacina_id=vacina_id, unidade_id=unidade_id, data_aplicacao=data_aplicacao)
    db.add(db_aplicacao)
    db.commit()
    db.refresh(db_aplicacao)
    return db_aplicacao

def delete_aplicacao(db: Session, aplicacao_id: int):
    db_aplicacao = db.query(Aplicacao).filter(Aplicacao.id == aplicacao_id).first()
    if db_aplicacao:
        db.delete(db_aplicacao)
        db.commit()
    return db_aplicacao