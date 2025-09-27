# app.py

import dash
import dash_bootstrap_components as dbc
from src.components.layout import layout
# Futuramente, importaremos aqui os callbacks para dar vida à aplicação

# Inicializa a aplicação Dash com um tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define o layout da aplicação
app.layout = layout

# Define o título da aba do navegador
app.title = "Análise ONS"

# Bloco principal para rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)