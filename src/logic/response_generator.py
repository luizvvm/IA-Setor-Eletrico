# src/logic/response_generator.py

import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table

def generate_response_components(ai_answer: str, df: pd.DataFrame = None, primary_color: str = "#4cd45d", text_color_dark: str = "#333333", card_bg_color: str = "#F0F0F0"):
    """
    Gera os componentes Dash para exibir a resposta da IA e o DataFrame,
    alinhado com o design Positivus-inspired.
    """
    # Componente para a resposta principal da IA (Lea)
    main_answer_component = dcc.Markdown(
        f"**Lea:** {ai_answer}", # Adiciona o nome da IA
        className="mb-3",
        style={'fontSize': '1.05rem', 'lineHeight': '1.6'} # Estilo do texto da IA
    )

    # Componente para os dados brutos (se existirem)
    data_details_component = html.Div()
    if df is not None and not df.empty:
        # Prepara a DataTable com o estilo clean
        data_table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10, # Limita o número de linhas exibidas por página
            page_action="native",
            sort_action="native",
            filter_action="native",
            style_table={
                'overflowX': 'auto',
                'border': f'1px solid {card_bg_color}', # Borda da tabela
                'borderRadius': '8px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.05)',
            },
            style_header={
                'backgroundColor': primary_color, # Fundo do cabeçalho da tabela com a cor primária
                'color': 'white',
                'fontWeight': 'bold',
                'borderBottom': 'none', # Remove a borda inferior do cabeçalho
                'padding': '12px 15px',
                'fontSize': '0.95rem',
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#fcfcfc'}, # Linhas alternadas
                {'if': {'row_index': 'even'}, 'backgroundColor': 'white'},
            ],
            style_cell={
                'padding': '10px 15px',
                'textAlign': 'left',
                'fontFamily': '"Poppins", sans-serif',
                'color': text_color_dark,
                'border': 'none', # Remove bordas internas das células
            }
        )

        # Acordeão para a tabela
        data_details_component = dbc.Accordion(
            [
                dbc.AccordionItem(
                    children=[data_table],
                    title=f"Ver {len(df)} linhas de dados brutos",
                    item_id="dados-brutos-item",
                    style={
                        '--bs-accordion-bg': 'white', # Fundo do item do acordeão
                        '--bs-accordion-color': text_color_dark,
                        '--bs-accordion-active-bg': primary_color, # Cor de fundo do cabeçalho quando ativo
                        '--bs-accordion-active-color': 'white', # Cor do texto do cabeçalho quando ativo
                        '--bs-accordion-btn-focus-border-color': primary_color,
                        '--bs-accordion-btn-focus-box-shadow': 'none', # Remove sombra de foco padrão
                        'borderRadius': '8px', # Arredondamento
                        'overflow': 'hidden',
                        'border': 'none' # Remove borda do item
                    },
                    className="shadow-sm" # Sombra leve para o acordeão
                ),
            ],
            start_collapsed=True,
            flush=True, # Remove bordas externas para um look mais clean
            className="mt-3",
            style={'borderRadius': '10px', 'border': 'none'} # Arredondamento e sem borda externa
        )

    # Retorna uma lista de componentes
    return [main_answer_component, data_details_component]