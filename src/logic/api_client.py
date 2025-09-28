# src/logic/api_client.py

import requests
import json

CKAN_API_BASE_URL = "https://dados.ons.org.br/api/3/action/"

def get_all_datasets_from_api():
    print("[API Client] Buscando a lista completa de datasets na API CKAN...")
    try:
        response = requests.get(f"{CKAN_API_BASE_URL}current_package_list_with_resources")
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            print(f"[API Client] Encontrados {len(data['result'])} datasets.")
            return data["result"]
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"[API Client] Erro de conexão ao buscar datasets: {e}")
        return []

def format_datasets_for_llm(datasets: list) -> list:
    """
    Formata a lista da API para um formato simples, mostrando todos os
    recursos (arquivos) disponíveis para cada dataset.
    """
    formatted_list = []
    for dataset in datasets:
        resources = []
        for resource in dataset.get("resources", []):
            # Adicionamos todos os formatos relevantes e suas URLs
            if resource.get("format", "").upper() in ['CSV', 'XLSX']:
                resources.append({
                    "name": resource.get("name"),
                    "format": resource.get("format", "").upper(),
                    "url": resource.get("url")
                })

        formatted_list.append({
            "id": dataset.get("name"),
            "title": dataset.get("title"),
            "notes": dataset.get("notes"),
            "resources": resources # A lista de arquivos agora tem múltiplos formatos
        })
    return formatted_list