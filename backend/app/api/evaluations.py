from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.entities import EntregaEstudiante, Rubrica, EvaluacionResultado
from app.schemas.evaluation_schema import EvaluacionIAStructuredOutput
from app.services.grading_service import DeterministicGradingEngine
# Aquí importarías tu cliente de IA (ej: Google GenAI o Ollama local)

router = APIRouter(prefix="/evaluaciones", tags=["Evaluacion Inteligente"])

@router.post("/ejecutar/{entrega_id}")
def evaluar_entrega_estudiante(entrega_id: int, db: Session = Depends(None)): # Inyecta tu sesión de DB
    # 1. Buscar la entrega y su rúbrica asociada
    entrega = db.query(EntregaEstudiante).filter(EntregaEstudiante.id == entrega_id).first()
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega no encontrada.")
    
    rubrica = db.query(Rubrica).filter(Rubrica.laboratorio_id == entrega.laboratorio_id).first()
    if not rubrica:
        raise HTTPException(status_code=404, detail="Rúbrica no configurada para este laboratorio.")
    
    pesos_rubrica = json.loads(rubrica.criterios_json) # Ej: {"criterio_1": 0.5, "criterio_2": 0.5}
    
    # 2. Simulación de respuesta estructurada del LLM (aquí integrarías tu llamada al modelo con Pydantic)
    # El LLM analiza el PDF y el código, devolviendo un JSON validado por EvaluacionIAStructuredOutput
    analisis_ia_mock = {
        "resumen_analisis": "El estudiante aplicó correctamente los conceptos...",
        "criterios": [
            {"criterio_id": "criterio_1", "nivel_desempeno": "Excelente", "puntaje_proporcional": 4.5, "evidencia_encontrada": "Línea 45 del script", "retroalimentacion": "Muy bien implementado"},
            {"criterio_id": "criterio_2", "nivel_desempeno": "Sobresaliente", "puntaje_proporcional": 4.0, "evidencia_encontrada": "Informe sección 2", "retroalimentacion": "Sólido análisis"}
        ],
        "fortalezas": ["Buena estructura de código"],
        "debilidades": ["Faltó comentar algunas funciones"],
        "recomendaciones": ["Mejorar la documentación interna"]
    }
    
    # 3. Calcular la nota de forma DETERMINISTA mediante el backend
    nota_calculada = DeterministicGradingEngine.calcular_nota_final(analisis_ia_mock, pesos_rubrica)
    
    # 4. Persistir el resultado de la evaluación en la base de datos
    nueva_evaluacion = EvaluacionResultado(
        entrega_id=entrega.id,
        nota_final=nota_calculada,
        detalles_json=json.dumps(analisis_ia_mock),
        modelo_utilizado="llama-3.2-local / gemini-1.5-pro"
    )
    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)
    
    return {
        "status": "success",
        "entrega_id": entrega_id,
        "nota_final_calculada": nota_calculada,
        "evaluacion_detallada": analisis_ia_mock
    }