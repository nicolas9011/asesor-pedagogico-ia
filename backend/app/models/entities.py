from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Laboratorio(Base):
    __tablename__ = "laboratorios"
    
    id = Column(Integer, primary_key=True, index=True)
    cohorte = Column(String(50), nullable=False) # Cohorte 1 o 2
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    rubrica = relationship("Rubrica", back_populates="laboratorio", uselist=False)
    entregas = relationship("EntregaEstudiante", back_populates="laboratorio")

class Rubrica(Base):
    __tablename__ = "rubricas"
    
    id = Column(Integer, primary_key=True, index=True)
    laboratorio_id = Column(Integer, ForeignKey("laboratorios.id"), unique=True)
    criterios_json = Column(Text, nullable=False) # Almacena la estructura de criterios y pesos (deben sumar 100%)
    
    laboratorio = relationship("Laboratorio", back_populates="rubrica")

class EntregaEstudiante(Base):
    __tablename__ = "entregas_estudiantes"
    
    id = Column(Integer, primary_key=True, index=True)
    laboratorio_id = Column(Integer, ForeignKey("laboratorios.id"))
    estudiante_id = Column(String(100), nullable=False)
    codigo_fuente_path = Column(String(255), nullable=True)
    informe_pdf_path = Column(String(255), nullable=True)
    estado = Column(String(50), default="PENDIENTE_EVALUACION") # PENDIENTE, APROBADA_DOCENTE
    
    laboratorio = relationship("Laboratorio", back_populates="entregas")
    evaluacion = relationship("EvaluacionResultado", back_populates="entrega", uselist=False)

class EvaluacionResultado(Base):
    __tablename__ = "evaluacion_resultados"
    
    id = Column(Integer, primary_key=True, index=True)
    entrega_id = Column(Integer, ForeignKey("entregas_estudiantes.id"), unique=True)
    nota_final = Column(Float, nullable=False) # Calculada determinísticamente (0.0 - 5.0)
    detalles_json = Column(Text, nullable=False) # Retroalimentación y desglose de la IA
    modelo_utilizado = Column(String(100), nullable=False)
    fecha_evaluacion = Column(DateTime, default=datetime.utcnow)
    
    entrega = relationship("EntregaEstudiante", back_populates="evaluacion")