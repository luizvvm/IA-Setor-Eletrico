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
        f"**Lea:** {ai_answer}", 
        className="mb-3",
        style={'fontSize': '1.05rem', 'lineHeight': '1.6'}
    )

    # Componente para os dados brutos 
    data_details_component = html.Div()
    if df is not None and not df.empty:
        # Prepara a DataTable com o estilo clean
        data_table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            page_action="native",
            sort_action="native",
            filter_action="native",
            style_table={
                'overflowX': 'auto',
                'border': f'1px solid {card_bg_color}', 
                'borderRadius': '8px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.05)',
            },
            style_header={
                'backgroundColor': primary_color, 
                'color': 'white',
                'fontWeight': 'bold',
                'borderBottom': 'none', 
                'padding': '12px 15px',
                'fontSize': '0.95rem',
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#fcfcfc'}, 
                {'if': {'row_index': 'even'}, 'backgroundColor': 'white'},
            ],
            style_cell={
                'padding': '10px 15px',
                'textAlign': 'left',
                'fontFamily': '"Poppins", sans-serif',
                'color': text_color_dark,
                'border': 'none',
            }
        )

        data_details_component = dbc.Accordion(
            [
                dbc.AccordionItem(
                    children=[data_table],
                    title=f"Ver {len(df)} linhas de dados brutos",
                    item_id="dados-brutos-item",
                    style={
                        '--bs-accordion-bg': 'white',
                        '--bs-accordion-color': text_color_dark,
                        '--bs-accordion-active-bg': primary_color, 
                        '--bs-accordion-active-color': 'white',
                        '--bs-accordion-btn-focus-border-color': primary_color,
                        '--bs-accordion-btn-focus-box-shadow': 'none', 
                        'borderRadius': '8px', 
                        'overflow': 'hidden',
                        'border': 'none' 
                    },
                    className="shadow-sm"
                ),
            ],
            start_collapsed=True,
            flush=True, 
            className="mt-3",
            style={'borderRadius': '10px', 'border': 'none'} 
        )

    return [main_answer_component, data_details_component]