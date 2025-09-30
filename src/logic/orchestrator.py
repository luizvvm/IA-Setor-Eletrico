# src/logic/orchestrator.py

import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
from src.logic.api_client import get_all_datasets_from_api, format_datasets_for_llm
from src.logic.intent_engine import get_intent_from_gemini, configure_gemini
from src.logic.data_collector import fetch_and_combine_data
from src.logic.insight_engine import get_insight_from_data

from src.logic.dataset_catalog import CURATED_DATASET

def run_query_pipeline(user_query: str, chat_history: list = []) -> dict:
    print("--- INICIANDO PIPELINE DE ORQUESTRAÇÃO (MODO SIMPLIFICADO) ---")

    # Configurar a API do Gemini
    try:
        configure_gemini()
    except ValueError as e:
        return {"answer": f"Erro de configuração da IA: {e}", "dataframe": None}

    # Obter o período (anos) da pergunta do usuário
    print("[Orquestrador] Extraindo período da pergunta do usuário...")
    period_plan = get_intent_from_gemini(user_query) # Chamada corrigida
    
    if "error" in period_plan or "start_year" not in period_plan:
        error_message = period_plan.get("error", "Não consegui identificar o período na sua pergunta.")
        return {"answer": error_message, "dataframe": None}

    start_year = period_plan["start_year"]
    end_year = period_plan["end_year"]
    print(f"[Orquestrador] Período identificado: de {start_year} a {end_year}.")

    # Obter informações do dataset que queremos analisar (hardcoded msm)
    # Por enquanto vamos trabalhar com todas as perguntas desse dataset mesmo
    dataset_info = CURATED_DATASET
    
    # Acionar o coletor de dados com os parâmetros corretos
    print(f"\n[Orquestrador] Acionando o coletor de dados...")
    final_df = fetch_and_combine_data(
        dataset_slug=dataset_info["slug"],
        file_prefix=dataset_info["file_prefix"],
        start_year=start_year,
        end_year=end_year,
        extension=dataset_info["extension"]
    )
    
    # Gerar o insight se os dados foram coletados com sucesso
    if final_df is not None and not final_df.empty:
        print("\n[Orquestrador] Enviando dados para o motor de insights...")
        
        # O insight_engine precisa do dataset_id, vamos passá-lo
        text_answer = get_insight_from_data(user_query, final_df, dataset_info["id"])
        
        return {"answer": text_answer, "dataframe": final_df.to_dict('records')} # É uma boa prática enviar o df como dict
    else:
        return {
            "answer": f"Não consegui baixar ou processar os dados de {start_year} a {end_year}. Os arquivos podem estar indisponíveis ou o período solicitado pode não ter dados.", 
            "dataframe": None
        }