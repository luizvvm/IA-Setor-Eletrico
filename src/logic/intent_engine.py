# src/logic/intent_engine.py

import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import pathlib
import pandas as pd
from google.api_core import exceptions as google_exceptions

WORKING_GEMINI_MODEL = "gemini-2.5-flash-lite"

def configure_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A chave da API do Gemini não foi encontrada.")
    genai.configure(api_key=api_key)

def _extract_json_from_response(text: str) -> dict:
    try:
        json_start_index = text.find('{')
        if json_start_index == -1: return {"error": "JSON não encontrado"}
        json_end_index = text.rfind('}')
        if json_end_index == -1: return {"error": "Fim do JSON não encontrado"}
        json_str = text[json_start_index : json_end_index + 1]
        return json.loads(json_str)
    except json.JSONDecodeError:
        raise

def get_intent_from_gemini(user_query: str, catalog_data: list, chat_history: list = []) -> dict:
    model = genai.GenerativeModel(WORKING_GEMINI_MODEL)
    
    # Pegamos os detalhes do nosso único dataset
    dataset_info = catalog_data[0]

    prompt = f"""
    Sua única função é extrair o período de tempo (ano de início e fim) da pergunta do usuário.
    O usuário sempre estará perguntando sobre o dataset de 'Indicadores de Disponibilidade de Geração'.

    - Se o usuário mencionar apenas um ano, use-o como ano de início e fim.
    - Se o usuário não mencionar um ano, use o ano atual ({pd.Timestamp.now().year}) como padrão.
    - Ignore os meses. A análise será sempre anual.

    Retorne um ÚNICO objeto JSON com as chaves "start_year" e "end_year". NADA MAIS.

    Pergunta do Usuário:
    "{user_query}"

    JSON de Saída:
    """

    print("--- Enviando prompt focado para o Gemini... ---")
    
    try:
        request_options = {"timeout": 60}
        response = model.generate_content(prompt, request_options=request_options)
        print(f"--- Resposta bruta recebida ---\n{response.text}")
        
        # Extrai o período (start_year, end_year)
        period_plan = _extract_json_from_response(response.text)

        # Monta o plano de ação completo, adicionando os dados fixos do nosso dataset
        action_plan = {
            "dataset_id": dataset_info["id"],
            "dataset_slug": dataset_info["slug"],
            "file_prefix": dataset_info["file_prefix"],
            "extension": dataset_info["extension"],
            "frequency": dataset_info["frequency"],
            "start_year": period_plan.get("start_year"),
            "end_year": period_plan.get("end_year")
        }
        
        # Retorna a estrutura completa que o orquestrador espera
        return {"intent": "fetch_and_analyze", "action_plan": action_plan}

    except Exception as e:
        print(f"Erro ao obter ou processar a intenção da IA: {e}")
        return {"error": f"Ocorreu um erro ao interpretar sua pergunta: {e}"}