import json
from typing import Dict, Any

class DeterministicGradingEngine:
    @staticmethod
    def calcular_nota_final(evaluacion_llm: Dict[str, Any], rubrica_definicion: Dict[str, float]) -> float:
        """
        Calcula de forma matemática y determinista la nota final (0.0 - 5.0) 
        multiplicando el puntaje de cada criterio por su peso porcentual en la rúbrica.
        
        :param evaluacion_llm: Diccionario deserializado del JSON estructurado del LLM.
        :param rubrica_definicion: Dict con {criterio_id: peso_porcentual} (ej: {"codigo": 0.4, "informe": 0.6} que sumen 1.0).
        """
        puntaje_total_ponderado = 0.0
        peso_acumulado = 0.0

        criterios_evaluados = {c["criterio_id"]: c for c in evaluacion_llm.get("criterios", [])}

        for criterio_id, peso in rubrica_definicion.items():
            if criterio_id in criterios_evaluados:
                # Obtenemos la nota dada al criterio (0.0 a 5.0)
                nota_criterio = float(criterios_evaluados[criterio_id].get("puntaje_proporcional", 0.0))
                
                # Acumulamos el valor ponderado
                puntaje_total_ponderado += nota_criterio * peso
                peso_acumulado += peso

        # Validación de seguridad por si la suma de pesos no da el 100% (1.0)
        if peso_acumulado <= 0:
            return 0.0

        nota_final = puntaje_total_ponderado / peso_acumulado
        
        # Redondear a 2 decimales y asegurar límites entre 0.0 y 5.0
        return round(max(0.0, min(5.0, nota_final)), 2)