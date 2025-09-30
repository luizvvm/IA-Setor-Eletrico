# Datathon ONS 2025 - Grupo 10

## Sobre o Desafio

O desafio proposto consiste em utilizar os dados abertos do Operador Nacional do Sistema Elétrico (ONS) para desenvolver soluções que gerem valor e insights para o setor e a sociedade.

Nossa solução, a **LumIA**, aborda este desafio através de uma plataforma de IA conversacional que democratiza o acesso à informação. A ferramenta permite que usuários consultem dados complexos sobre a disponibilidade de usinas em linguagem natural, recebendo respostas claras e análises em um dashboard interativo, promovendo assim a transparência e a "cidadania energética".

## Estrutura do Repositório

A estrutura de pastas deste repositório foi organizada para manter o projeto limpo e modular.

- `data/`: Contém os datasets brutos, processados e externos.
- `docs/`: Documentação do projeto, relatórios e apresentações.
- `notebooks/`: Notebooks Jupyter para exploração de dados, modelagem e análise.
- `src/`: Código fonte, scripts e módulos reutilizáveis.
- `results/`: Resultados finais, como submissões, visualizações e modelos treinados.

## Como Começar

**Pré-requisitos:**
* Python 3.9+
* Uma chave de API do Google Gemini configurada no arquivo `.env` como `GEMINI_API_KEY`.

1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:DatathONS2025/grupo10.git
    cd grupo10
    ```

2.  **Restaure as dependências:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Execute o projeto:**

    ```bash
    python app.py
    ```
    A aplicação estará disponível em `http://127.0.0.1:8050/` no seu navegador.



## Contribuidores

- Luiz Vitor Vieira de Mattos (luizvvm)