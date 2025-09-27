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

def get_intent_from_gemini(user_query: str, catalog_data: list) -> dict:
    model = genai.GenerativeModel(WORKING_GEMINI_MODEL)
    catalog_str = json.dumps(catalog_data, indent=2, ensure_ascii=False)

    # --- PROMPT DE CLASSIFICAÇÃO DE INTENÇÃO ---
    prompt = f"""
    Sua primeira e mais importante tarefa é classificar a intenção do usuário em uma de três categorias: 'list_datasets', 'describe_dataset', ou 'fetch_and_analyze'.

    - Use 'list_datasets' se o usuário perguntar quais datasets estão disponíveis.
    - Use 'describe_dataset' se o usuário perguntar sobre o que é um dataset específico (ex: "fala sobre o que?", "o que são os dados de...?").
    - Use 'fetch_and_analyze' para todas as outras perguntas que exigem busca e análise de dados (ex: "qual foi o intercâmbio em 2023?").

    Depois de definir a intenção, siga as regras para cada uma:

    1. Se a intenção for 'list_datasets':
       Retorne APENAS: {{"intent": "list_datasets"}}

    2. Se a intenção for 'describe_dataset':
       - Encontre o dataset no catálogo que melhor corresponde à pergunta do usuário.
       - Retorne APENAS: {{"intent": "describe_dataset", "dataset_title": "título do dataset escolhido"}}

    3. Se a intenção for 'fetch_and_analyze':
       - Encontre o MELHOR dataset no catálogo para responder a pergunta.
       - Extraia os parâmetros: 'dataset_slug', 'file_prefix', 'extension'.
       - Extraia o período em anos. Se não houver, use o ano atual ({pd.Timestamp.now().year}).
       - Determine a frequência ('monthly' ou 'yearly') baseado nos nomes dos arquivos no catálogo.
       - Retorne o JSON completo: {{"intent": "fetch_and_analyze", "action_plan": {{...todos os parâmetros...}}}}

    **Catálogo de Datasets Disponíveis:**
    ```json
    {catalog_str}
    ```

    **Pergunta do Usuário:**
    "{user_query}"

    **JSON de Saída:**
    """

    print("--- Enviando prompt de intenção para o Gemini (com timeout de 60s)... ---")
    
    try:
        request_options = {"timeout": 60}
        response = model.generate_content(prompt, request_options=request_options)
        response_text = response.text.strip().replace("```json", "").replace("```", "")
        print(f"--- Resposta de intenção recebida do Gemini ---\n{response_text}")
        intent_plan = json.loads(response_text)
        return intent_plan
    except Exception as e:
        print(f"Erro ao obter intenção da IA: {e}")
        return {"error": f"Ocorreu um erro ao interpretar sua pergunta: {e}"}