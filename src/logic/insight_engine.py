# src/logic/insight_engine.py

import pandas as pd
import google.generativeai as genai

WORKING_GEMINI_MODEL = "gemini-2.5-flash-lite"

def get_insight_from_data(user_query: str, df: pd.DataFrame, dataset_id: str) -> str:
    """
    Recebe os dados de disponibilidade e gera uma análise em texto.
    """
    model = genai.GenerativeModel(WORKING_GEMINI_MODEL)
    
    analysis_type = "Disponibilidade de Usinas"
    data_context = ""
    
    try:
        # --- LÓGICA DE ANÁLISE CORRIGIDA ---
        # 1. Procura pela coluna correta 'val_dispf'
        disponibilidade_col = 'val_dispf'
        if disponibilidade_col not in df.columns:
            return "Não encontrei a coluna 'val_dispf' nos dados para analisar a disponibilidade."

        # 2. Converte a coluna para numérico, tratando vírgulas como decimais e tratando erros
        if df[disponibilidade_col].dtype == 'object':
             df[disponibilidade_col] = df[disponibilidade_col].str.replace(',', '.', regex=False).astype(float)
        
        df.dropna(subset=[disponibilidade_col], inplace=True)

        # 3. Realiza a análise
        avg_by_usina = df.groupby('nom_usina')[disponibilidade_col].mean().sort_values(ascending=False)
        
        data_context += f"Resumo da Disponibilidade Média por Usina no período solicitado:\n"
        data_context += "\n**Usinas com Maior Disponibilidade Média:**\n"
        for usina, value in avg_by_usina.head(5).items():
            data_context += f"- {usina}: {value:.2f}%\n"
        
        data_context += "\n**Usinas com Menor Disponibilidade Média:**\n"
        for usina, value in avg_by_usina.tail(5).items():
            data_context += f"- {usina}: {value:.2f}%\n"
            
    except Exception as e:
        print(f"ERRO durante a pré-análise dos dados de disponibilidade: {e}")
        return "Desculpe, encontrei um erro ao tentar analisar os dados de disponibilidade. Verifique o formato do arquivo."

    # --- Montagem do Prompt Final ---
    prompt = f"""
    Você é um assistente de dados da ONS especialista em disponibilidade de usinas.
    Responda à pergunta do usuário usando o resumo pré-analisado fornecido.

    **Tipo de Análise Realizada:** {analysis_type}
    **Pergunta do Usuário:** "{user_query}"
    **Resumo dos Dados para sua Análise:**
    ```
    {data_context}
    ```
    **Sua Resposta:**
    Formule uma resposta clara em português, explicando os principais pontos. Destaque as usinas com maior e menor disponibilidade e o que isso pode significar.
    """

    print(f"--- Enviando contexto ({analysis_type}) para o Módulo de Insights... ---")
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao gerar insight: {e}")
        return "Desculpe, ocorreu um erro ao interpretar os dados."