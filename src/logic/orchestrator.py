# src/logic/orchestrator.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
from src.logic.api_client import get_all_datasets_from_api, format_datasets_for_llm
from src.logic.intent_engine import get_intent_from_gemini, configure_gemini
from src.logic.data_collector import fetch_and_combine_data
from src.logic.insight_engine import get_insight_from_data

def run_query_pipeline(user_query: str) -> dict:
    print("--- INICIANDO PIPELINE DE ORQUESTRAÇÃO INTELIGENTE ---")

    print("\n[Orquestrador] Buscando catálogo de datasets via API CKAN...")
    all_datasets = get_all_datasets_from_api()
    if not all_datasets:
        return {"answer": "Desculpe, não consegui me conectar ao portal de dados da ONS.", "dataframe": None}

    try:
        configure_gemini()
    except ValueError as e:
        return {"answer": f"Erro de configuração: {e}", "dataframe": None}

    # PASSO 1: Obter o plano de intenção da IA
    formatted_catalog = format_datasets_for_llm(all_datasets)
    intent_plan = get_intent_from_gemini(user_query, formatted_catalog)
    
    intent = intent_plan.get("intent")

    # PASSO 2: Agir com base na intenção
    if intent == "list_datasets":
        print("[Orquestrador] Intenção 'list_datasets' recebida. Respondendo diretamente.")
        titles = [ds.get('title', 'Sem título') for ds in all_datasets]
        answer = "Claro! Atualmente, eu tenho acesso aos seguintes conjuntos de dados da ONS:\n\n* " + "\n* ".join(titles)
        return {"answer": answer, "dataframe": None}

    elif intent == "describe_dataset":
        print("[Orquestrador] Intenção 'describe_dataset' recebida. Respondendo diretamente.")
        title_to_find = intent_plan.get("dataset_title")
        for ds in all_datasets:
            if ds.get('title') == title_to_find:
                answer = f"O conjunto de dados **'{ds.get('title')}'** fala sobre o seguinte:\n\n> {ds.get('notes', 'Nenhuma descrição detalhada disponível.')}"
                return {"answer": answer, "dataframe": None}
        return {"answer": "Desculpe, não encontrei um dataset com esse nome para descrever.", "dataframe": None}
        
    elif intent == "fetch_and_analyze":
        print("[Orquestrador] Intenção 'fetch_and_analyze' recebida. Iniciando busca de dados...")
        action_plan = intent_plan.get("action_plan")
        if not action_plan:
            return {"answer": "A IA decidiu buscar os dados, mas não conseguiu criar um plano de ação.", "dataframe": None}

        print("\n[Orquestrador] Acionando o coletor de dados...")
        final_df = fetch_and_combine_data(**action_plan)

        if final_df is not None and not final_df.empty:
            print("\n[Orquestrador] Enviando dados para o motor de insights...")
            text_answer = get_insight_from_data(user_query, final_df)
            return {"answer": text_answer, "dataframe": final_df}
        else:
            return {"answer": "Não foi possível encontrar dados para a sua pergunta. Verifique os anos solicitados.", "dataframe": None}

    else:
        # Caso a IA retorne uma intenção desconhecida ou um erro
        return {"answer": f"Desculpe, não entendi o que fazer com a sua pergunta. A IA retornou o seguinte plano: {intent_plan}", "dataframe": None}