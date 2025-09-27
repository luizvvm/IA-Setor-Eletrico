# src/logic/api_client.py

import requests
import json

# URL base da API CKAN para o portal de Dados Abertos da ONS
CKAN_API_BASE_URL = "https://dados.ons.org.br/api/3/action/"

def get_all_datasets_from_api():
    """
    Busca a lista de todos os datasets (pacotes) disponíveis na API da ONS.
    Retorna uma lista de dicionários, cada um representando um dataset.
    """
    print("[API Client] Buscando a lista completa de datasets na API CKAN...")
    try:
        # A função 'current_package_list_with_resources' retorna os datasets e seus arquivos
        response = requests.get(f"{CKAN_API_BASE_URL}current_package_list_with_resources")
        response.raise_for_status()
        
        data = response.json()
        if data.get("success"):
            print(f"[API Client] Encontrados {len(data['result'])} datasets.")
            return data["result"]
        else:
            print(f"[API Client] A API retornou um erro: {data.get('error')}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"[API Client] Erro de conexão ao buscar datasets: {e}")
        return []

def format_datasets_for_llm(datasets: list) -> list:
    """
    Formata a lista complexa de datasets da API para um formato simples e limpo,
    ideal para ser enviado como contexto para o Gemini.
    """
    formatted_list = []
    for dataset in datasets:
        # Para cada dataset, pegamos informações importantes
        formatted_list.append({
            "id": dataset.get("name"),  # 'name' é o ID único, ex: 'intercambio_modalidade_ho'
            "title": dataset.get("title"), # Título legível, ex: 'Dados de Intercâmbio...'
            "notes": dataset.get("notes"), # A descrição longa
            # Extraímos os links diretos para os arquivos CSV, se existirem
            "resources": [
                {
                    "name": resource.get("name"),
                    "url": resource.get("url")
                }
                for resource in dataset.get("resources", [])
                if resource.get("format", "").upper() == 'CSV' # Filtramos para pegar só CSVs
            ]
        })
    return formatted_list

# --- Bloco de Teste ---
if __name__ == '__main__':
    all_datasets = get_all_datasets_from_api()
    if all_datasets:
        # Mostra os detalhes do primeiro dataset encontrado como exemplo
        print("\n--- Exemplo de dados brutos do primeiro dataset ---")
        print(json.dumps(all_datasets[0], indent=2, ensure_ascii=False))

        print("\n\n--- Exemplo do mesmo dataset formatado para a IA ---")
        formatted_datasets = format_datasets_for_llm(all_datasets)
        print(json.dumps(formatted_datasets[0], indent=2, ensure_ascii=False))