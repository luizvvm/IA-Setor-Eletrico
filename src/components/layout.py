# src/components/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc

# Layout principal da aplicação
layout = dbc.Container([
    # Linha 1: Título
    dbc.Row(
        dbc.Col(
            html.H1("Análise Inteligente de Dados da ONS", className="text-center text-primary mb-4"),
            width=12
        )
    ),

    # Linha 2: Campo de entrada e botão
    dbc.Row(
        [
            dbc.Col(
                dbc.Input(id="user-input", type="text", placeholder="Faça uma pergunta sobre os dados do setor elétrico...", size="lg"),
                width=10
            ),
            dbc.Col(
                dbc.Button("Analisar", id="submit-button", color="primary", size="lg"),
                width=2
            ),
        ],
        className="mb-4"
    ),

    # Linha 3: Área de resultados
    dbc.Row(
        dbc.Col(
            dcc.Loading( # Adiciona um ícone de "carregando" enquanto a resposta é processada
                id="loading-component",
                children=[
                    html.Div(id="results-output") # Aqui aparecerão os gráficos e textos
                ],
                type="default"
            ),
            width=12
        )
    )
], fluid=True)