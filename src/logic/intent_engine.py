# src/logic/intent_engine.py
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import pandas as pd

WORKING_GEMINI_MODEL = "gemini-2.5-flash-lite"

def configure_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: raise ValueError("Chave da API do Gemini não encontrada.")
    genai.configure(api_key=api_key)

def _extract_json_from_response(text: str) -> dict:
    try:
        json_start_index = text.find('{')
        if json_start_index == -1: return {"error": "JSON não encontrado"}
        json_end_index = text.rfind('}')
        if json_end_index == -1: return {"error": "Fim do JSON não encontrado"}
        json_str = text[json_start_index : json_end_index + 1]
        return json.loads(json_str)
    except Exception as e:
        print(f"ERRO de extração de JSON: {e}\nResposta recebida:\n{text}")
        return {"error": "A IA retornou uma resposta em um formato inválido."}

def get_intent_from_gemini(user_query: str) -> dict:
    model = genai.GenerativeModel(WORKING_GEMINI_MODEL)
    
    prompt = f"""
    Sua única função é extrair o período de tempo (ano de início e fim) da pergunta do usuário.
    O usuário sempre estará perguntando sobre o dataset de 'Indicadores de Disponibilidade de Geração'.

    - Se o usuário mencionar apenas um ano, use-o como ano de início e fim.
    - Se o usuário não mencionar um ano, use o ano anterior ({pd.Timestamp.now().year - 1}) como padrão.
    - Se o usuário mencionar um intervalo (ex: 'entre 2022 e 2024'), extraia o início e o fim.
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
        period_plan = _extract_json_from_response(response.text)
        return period_plan
    except Exception as e:
        print(f"Erro ao obter intenção da IA: {e}")
        return {"error": f"Ocorreu um erro ao interpretar sua pergunta: {e}"}