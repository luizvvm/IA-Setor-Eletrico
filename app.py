# app.py

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc

# Importa o nosso orquestrador e gerador de resposta
from src.logic.orchestrator import run_query_pipeline
from src.logic.response_generator import generate_response_layout

# --- Correção de Importação (garante que os módulos são encontrados) ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Inicializa a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = "Assistente ONS de Dados"

# --- Novo Layout com Estilo de Chat ---
app.layout = dbc.Container([
    # Título da Aplicação
    dbc.Row(dbc.Col(html.H1("Assistente ONS de Dados", className="text-center my-4 text-primary"))),

    # Área de Histórico de Conversas (onde as perguntas e respostas aparecem)
    dbc.Row(dbc.Col(
        html.Div(id="chat-history", 
                 style={"height": "70vh", "overflowY": "auto", "border": "1px solid #dee2e6", "borderRadius": "5px", "padding": "15px", "backgroundColor": "#f8f9fa"}),
        width=12
    )),

    # Área de Entrada do Usuário e Botão (fixa na parte inferior)
    dbc.Row(dbc.Col(
        dbc.InputGroup([
            dbc.Input(id="user-input", placeholder="Faça sua pergunta...", type="text", debounce=True),
            dbc.Button("Analisar", id="submit-button", color="primary", className="ms-2")
        ], className="my-3"),
        width=12
    )),

    # Componente para armazenar o histórico de dados no cliente (não visível)
    # Isso é crucial para manter o estado do chat entre as interações
    dcc.Store(id='store-chat-history', data=[])

], fluid=True, style={"height": "100vh", "display": "flex", "flexDirection": "column"}) # Layout flex para fixar a barra de entrada


# --- O CALLBACK DO CHAT ---
@app.callback(
    Output("chat-history", "children"),     # Atualiza o histórico visível
    Output("store-chat-history", "data"),   # Atualiza o histórico de dados
    Output("user-input", "value"),          # Limpa a caixa de entrada
    Input("submit-button", "n_clicks"),
    State("user-input", "value"),
    State("store-chat-history", "data"),    # Lemos o histórico anterior
    prevent_initial_call=True
)
def handle_chat_input(n_clicks, user_query, current_chat_history):
    if not user_query:
        # Se a pergunta for vazia, apenas retorna o histórico sem alterações e a caixa vazia
        return current_chat_history, current_chat_history, ""

    # Adiciona a pergunta do usuário ao histórico (estilo "chat")
    current_chat_history.append({"speaker": "user", "message": user_query})
    
    # Adiciona uma mensagem de "digitando..." ou "processando..."
    processing_message_id = f"processing-{n_clicks}"
    current_chat_history.append({"speaker": "ai", "message": html.Div("Processando sua solicitação...", id=processing_message_id)})
    
    # Atualiza a interface imediatamente com a pergunta e a mensagem de processamento
    # Para que o usuário veja a resposta da sua própria pergunta instantaneamente
    output_history_layout = [
        html.Div([
            html.Div(f"{item['speaker'].title()}:", className="fw-bold"),
            html.Div(item['message'], className="mb-2")
        ], className=f"text-{ 'end' if item['speaker'] == 'user' else 'start' } border-bottom pb-2 mb-2")
        for item in current_chat_history
    ]
    
    # --- Aqui a mágica acontece: chamamos nosso backend ---
    final_dataframe = run_query_pipeline(user_query)
    response_layout = generate_response_layout(final_dataframe)

    # Remove a mensagem de "processando..." e adiciona a resposta real
    current_chat_history.pop() # Remove a mensagem de processamento
    current_chat_history.append({"speaker": "ai", "message": response_layout})

    # Prepara o layout final para exibição
    final_output_history_layout = [
        html.Div([
            html.Div(f"{item['speaker'].title()}:", className="fw-bold"),
            html.Div(item['message'], className="mb-2")
        ], className=f"text-{ 'end' if item['speaker'] == 'user' else 'start' } border-bottom pb-2 mb-2")
        for item in current_chat_history
    ]

    # Retorna o histórico atualizado, os dados do histórico e limpa a caixa de entrada
    return final_output_history_layout, current_chat_history, ""

# Bloco principal para rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)