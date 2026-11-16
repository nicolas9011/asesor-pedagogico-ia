from pydantic import BaseModel, Field
from typing import List, Dict

class CriterioEvaluadoLLM(BaseModel):
    criterio_id: str = Field(..., description="ID o nombre corto del criterio según la rúbrica")
    nivel_desempeno: str = Field(..., description="Insuficiente, Aceptable, Sobresaliente, Excelente")
    puntaje_proporcional: float = Field(..., ge=0.0, le=5.0, description="Puntuación de 0.0 a 5.0 asignada a este criterio por la IA")
    evidencia_encontrada: str = Field(..., description="Cita exacta del código o informe del estudiante")
    retroalimentacion: str

class EvaluacionIAStructuredOutput(BaseModel):
    resumen_analisis: str = Field(..., description="Análisis general de qué aprendió el estudiante y cómo aplicó los conocimientos")
    criterios: List[CriterioEvaluadoLLM]
    fortalezas: List[str]
    debilidades: List[str]
    recomendaciones: List[str]