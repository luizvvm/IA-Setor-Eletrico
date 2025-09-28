# --- Importações e Configuração do Path ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd # Adicionado para manipulação de DataFrame

from src.logic.orchestrator import run_query_pipeline
from src.logic.response_generator import generate_response_components

# --- Paleta de Cores e Configurações Iniciais ---
PRIMARY_COLOR = "#4cd45d"
BACKGROUND_WHITE = "#FFFFFF"
TEXT_COLOR_DARK = "#333333"
CARD_AI_BG_COLOR = "#F0F0F0"
CARD_USER_BG_COLOR = PRIMARY_COLOR

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "LumIA"

# --- Layout do Aplicativo ---
app.layout = dbc.Container(
    fluid=True,
    style={
        'backgroundColor': BACKGROUND_WHITE,
        'minHeight': '100vh',
        'fontFamily': '"Poppins", sans-serif',
        'color': TEXT_COLOR_DARK,
        'padding': '0',
    },
    children=[
        # --- Barra Superior (Header) ---
        html.Header(
            style={
                'backgroundColor': PRIMARY_COLOR,
                'padding': '1.2rem 2.5rem',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'space-between',
                'borderBottomLeftRadius': '15px',
                'borderBottomRightRadius': '15px',
            },
            children=[
                html.Div(
                    style={'display': 'flex', 'alignItems': 'center'},
                    children=[
                        html.Img(
                            src=app.get_asset_url('logo.png'),
                            height="55px",
                            style={'marginRight': '15px', 'borderRadius': '8px'}
                        ),
                        html.H2(
                            "LumIA",
                            style={'color': BACKGROUND_WHITE, 'fontWeight': 'bold', 'marginBottom': '0'}
                        )
                    ]
                ),
                html.H4(
                    "Hackathon ONS 2024",
                    style={'color': BACKGROUND_WHITE, 'fontSize': '1.3rem', 'opacity': '0.9', 'marginBottom': '0'},
                    className="d-none d-md-block"
                )
            ]
        ),

        # --- Área Principal do Chat ---
        dbc.Container(
            className="my-5",
            style={'maxWidth': '900px'},
            children=[
                dbc.Row(justify="center", children=[
                    dbc.Col(
                        children=[
                            dcc.Store(id='chat-history-store', data=[]),
                            html.Div(
                                id='chat-history-display',
                                style={
                                    'minHeight': '55vh',
                                    'maxHeight': '70vh',
                                    'overflowY': 'auto',
                                    'padding': '2rem',
                                    'border': f'1px solid {CARD_AI_BG_COLOR}',
                                    'borderRadius': '15px',
                                    'backgroundColor': BACKGROUND_WHITE,
                                    'boxShadow': '0 8px 30px rgba(0,0,0,0.08)',
                                    'marginBottom': '2rem',
                                    'display': 'flex',
                                    'flexDirection': 'column',
                                    'gap': '1.5rem',
                                }
                            ),
                            
                            dcc.Loading(
                                id="loading-spinner",
                                type="dot",
                                color=PRIMARY_COLOR,
                                children=html.Div(id="loading-output-placeholder", style={'height': '20px', 'marginBottom': '1rem'})
                            ),
                            
                            dbc.InputGroup(
                                style={'height': '60px'},
                                children=[
                                    dbc.Input(
                                        id='user-input',
                                        placeholder='Pergunte à Lea sobre disponibilidade de usinas...',
                                        n_submit=0,
                                        style={
                                            'borderRadius': '10px 0 0 10px',
                                            'border': f'1px solid {PRIMARY_COLOR}',
                                            'padding': '0.8rem 1.2rem',
                                            'fontSize': '1.1rem',
                                            'color': TEXT_COLOR_DARK,
                                            'backgroundColor': CARD_AI_BG_COLOR,
                                            'boxShadow': 'inset 0 1px 3px rgba(0,0,0,0.05)',
                                        }
                                    ),
                                    dbc.Button(
                                        "Analisar",
                                        id='submit-button',
                                        n_clicks=0,
                                        color="success",
                                        style={
                                            'backgroundColor': PRIMARY_COLOR,
                                            'borderColor': PRIMARY_COLOR,
                                            'color': BACKGROUND_WHITE,
                                            'borderRadius': '0 10px 10px 0',
                                            'fontWeight': 'bold',
                                            'fontSize': '1.1rem',
                                            'padding': '0.8rem 1.5rem',
                                            'boxShadow': '0 4px 10px rgba(0,0,0,0.1)',
                                        }
                                    ),
                                ]
                            ),
                        ]
                    )
                ])
            ]
        )
    ]
)
# Em app.py, substitua a função update_chat inteira por esta:

@app.callback(
    Output('chat-history-display', 'children'),
    Output('chat-history-store', 'data'),
    Output('user-input', 'value'),
    Output("loading-output-placeholder", "children"),
    Input('submit-button', 'n_clicks'),
    Input('user-input', 'n_submit'),
    State('user-input', 'value'),
    State('chat-history-store', 'data'),
    prevent_initial_call=True
)
def update_chat(n_clicks, n_submit, user_query, chat_history):
    if not user_query:
        return dash.no_update, dash.no_update, "", ""

    # Adiciona a pergunta do usuário ao histórico
    chat_history.append({'speaker': 'user', 'message': user_query})
    
    # Chama o pipeline para obter a resposta da IA
    pipeline_result = run_query_pipeline(user_query, chat_history)
    
    # --- CORREÇÃO APLICADA AQUI ---
    # Prepara a mensagem da IA para ser armazenada no dcc.Store
    ai_message_for_storage = {
        'answer': pipeline_result.get('answer'),
        'dataframe': None
    }
    # pipeline_result['dataframe'] já é uma lista de dicionários
    dataframe_list = pipeline_result.get('dataframe') 

    # Verifica se a lista existe e não está vazia
    if dataframe_list: 
        # Atribui a lista diretamente, pois ela já está no formato para armazenamento
        ai_message_for_storage['dataframe'] = dataframe_list
    # --- FIM DA CORREÇÃO ---

    # Adiciona a resposta da IA (já serializada) ao histórico
    chat_history.append({'speaker': 'ai', 'message': ai_message_for_storage})
    
    # Monta o layout de exibição do chat a partir do histórico completo
    chat_display_layout = []
    for item in chat_history:
        is_user = item['speaker'] == 'user'
        
        if is_user:
            message_content = html.P(item['message'], style={'marginBottom': '0', 'fontSize': '1.05rem'})
        else: # É a IA
            df_data = item['message'].get('dataframe')
            df = pd.DataFrame(df_data) if df_data is not None else None
            
            message_content = generate_response_components(
                item['message'].get('answer'), 
                df
            )

        card_style = {
            'width': 'fit-content',
            'maxWidth': '80%' if is_user else '85%',
            'backgroundColor': CARD_USER_BG_COLOR if is_user else CARD_AI_BG_COLOR,
            'color': BACKGROUND_WHITE if is_user else TEXT_COLOR_DARK,
            'borderRadius': '15px 15px 5px 15px' if is_user else '15px 15px 15px 5px',
            'padding': '12px 20px',
            'boxShadow': '0 4px 10px rgba(0,0,0,0.1)' if is_user else '0 4px 10px rgba(0,0,0,0.05)',
        }

        chat_display_layout.append(
            dbc.Card(
                dbc.CardBody(message_content),
                className="mb-3 ms-auto" if is_user else "mb-3 me-auto",
                style=card_style
            )
        )
    
    return chat_display_layout, chat_history, "", ""

# --- Bloco para Executar o Aplicativo ---
if __name__ == '__main__':
    app.run(debug=True)
