# src/logic/insight_engine.py

import pandas as pd
import google.generativeai as genai

# Usaremos o mesmo modelo que já funciona para você
WORKING_GEMINI_MODEL = "gemini-2.5-flash-lite" 

def get_insight_from_data(user_query: str, df: pd.DataFrame) -> str:
    """
    Recebe a pergunta original do usuário e um DataFrame, e usa a IA para
    gerar uma resposta em texto baseada nos dados.

    Args:
        user_query (str): A pergunta original do usuário.
        df (pd.DataFrame): O DataFrame com os dados coletados.

    Returns:
        str: Uma resposta em texto gerada pela IA.
    """
    model = genai.GenerativeModel(WORKING_GEMINI_MODEL)
    
    # --- Preparação dos Dados para a IA ---
    # Não podemos enviar 167 mil linhas para a IA.
    # Vamos enviar um resumo estatístico e as primeiras linhas como contexto.
    data_summary = df.describe(include='all').to_string()
    data_head = df.head(5).to_string()

    prompt = f"""
    Você é um assistente de análise de dados para jornalistas e leigos, trabalhando com dados do Operador Nacional do Sistema Elétrico (ONS). Sua tarefa é responder à pergunta do usuário de forma clara e direta, baseando-se exclusivamente nos dados fornecidos.

    **Pergunta Original do Usuário:**
    "{user_query}"

    **Dados extraídos para sua análise:**

    1. Resumo Estatístico dos Dados:
    ```
    {data_summary}
    ```

    2. Amostra das Primeiras Linhas dos Dados:
    ```
    {data_head}
    ```

    **Sua Resposta:**
    Responda à pergunta do usuário em português. Seja conciso e foque nos insights principais que os dados revelam. Se os dados permitirem, calcule totais, médias ou aponte tendências. NÃO invente informações. Se os dados não forem suficientes para responder, diga isso claramente.
    """

    print("--- Enviando dados para o Módulo de Insights (2ª chamada à IA)... ---")
    
    try:
        response = model.generate_content(prompt)
        print("--- Resposta em texto recebida! ---")
        return response.text
    except Exception as e:
        print(f"Erro ao gerar insight: {e}")
        return "Desculpe, ocorreu um erro ao tentar interpretar os dados."