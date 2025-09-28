# src/logic/orchestrator.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.logic.dataset_catalog import CURATED_DATASETS
from src.logic.intent_engine import get_intent_from_gemini, configure_gemini
from src.logic.data_collector import fetch_and_combine_data
from src.logic.insight_engine import get_insight_from_data

def run_query_pipeline(user_query: str, chat_history: list = []) -> dict:
    print("--- INICIANDO PIPELINE (MODO ESPECIALISTA) ---")

    try:
        configure_gemini()
    except ValueError as e:
        return {"answer": f"Erro de configuração: {e}", "dataframe": None}

    intent_plan = get_intent_from_gemini(user_query, CURATED_DATASETS, chat_history)
    
    if "error" in intent_plan or "action_plan" not in intent_plan:
        # Se não for um plano de ação, pode ser uma resposta direta
        if intent_plan.get("direct_answer"):
            return {"answer": intent_plan["direct_answer"], "dataframe": None}
        return {"answer": "Desculpe, não consegui entender o período de tempo na sua pergunta.", "dataframe": None}
    
    action_plan = intent_plan["action_plan"]
    
    # --- CORREÇÃO DO TypeError ---
    # 1. Guardamos o dataset_id para usar depois.
    dataset_id = action_plan.get("dataset_id")

    # 2. Criamos um dicionário SÓ com os argumentos que o data_collector espera.
    collector_args = {
        "dataset_slug": action_plan.get("dataset_slug"),
        "file_prefix": action_plan.get("file_prefix"),
        "extension": action_plan.get("extension"),
        "start_year": action_plan.get("start_year"),
        "end_year": action_plan.get("end_year"),
        "frequency": action_plan.get("frequency"),
    }
    
    # 3. Chamamos o data_collector com os argumentos filtrados.
    final_df = fetch_and_combine_data(**collector_args)
    # --- FIM DA CORREÇÃO ---

    if final_df is not None and not final_df.empty:
        text_answer = get_insight_from_data(user_query, final_df, dataset_id)
        return {"answer": text_answer, "dataframe": final_df}
    else:
        return {"answer": "Não foi possível encontrar dados para o período solicitado.", "dataframe": None}