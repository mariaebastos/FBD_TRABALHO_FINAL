from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database_config import Base # Importa a Base do arquivo de configuração

class Fabricante(Base):
    __tablename__ = 'fabricante'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    vacinas = relationship("Vacina", back_populates="fabricante")

class Vacina(Base):
    __tablename__ = 'vacina'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    fabricante_id = Column(Integer, ForeignKey('fabricante.id'))
    fabricante = relationship("Fabricante", back_populates="vacinas")
    aplicacoes = relationship("Aplicacao", back_populates="vacina")

class UnidadeSaude(Base):
    __tablename__ = 'unidade_saude'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    endereco = Column(String)
    aplicacoes = relationship("Aplicacao", back_populates="unidade")

class Paciente(Base):
    __tablename__ = 'paciente'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(Date)
    cpf = Column(String, unique=True)
    aplicacoes = relationship("Aplicacao", back_populates="paciente")

class Aplicacao(Base):
    __tablename__ = 'aplicacao'
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('paciente.id'))
    vacina_id = Column(Integer, ForeignKey('vacina.id'))
    unidade_id = Column(Integer, ForeignKey('unidade_saude.id'))
    data_aplicacao = Column(Date)

    paciente = relationship("Paciente", back_populates="aplicacoes")
    vacina = relationship("Vacina", back_populates="aplicacoes")
    unidade = relationship("UnidadeSaude", back_populates="aplicacoes")