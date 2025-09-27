import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table

def generate_response_layout(pipeline_result: dict):
    """
    Recebe o dicionário do pipeline (com a resposta em texto e o DataFrame) 
    e gera o layout de exibição para o chat.
    """
    if not pipeline_result or not isinstance(pipeline_result, dict):
        return dbc.Alert("Ocorreu um erro interno ao processar sua solicitação.", color="danger")

    text_answer = pipeline_result.get("answer", "Não foi possível gerar uma resposta em texto.")
    df = pipeline_result.get("dataframe")

    # Componente principal: A resposta em texto da IA.
    main_answer_component = dcc.Markdown(text_answer, className="mb-4")

    # Componente secundário: Os dados brutos, escondidos em um menu "sanfona".
    if df is not None and not df.empty:
        data_details_component = dbc.Accordion(
            [
                dbc.AccordionItem(
                    dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        page_size=10,
                        page_action="native",
                        sort_action="native",
                        filter_action="native",
                        style_table={'overflowX': 'auto'},
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                        ],
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    ),
                    title="Clique para ver os dados brutos utilizados na análise"
                )
            ],
            start_collapsed=True,
            flush=True,
        )
    else:
        data_details_component = html.Div() # Componente vazio se não houver dados

    # Retorna a resposta em texto e, opcionalmente, o menu com os dados
    return html.Div([
        main_answer_component,
        data_details_component
    ])