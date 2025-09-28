# src/logic/data_collector.py

import pandas as pd
import requests
import io
from typing import List, Optional

def fetch_and_combine_data(file_urls: List[str], sep: str = ';') -> Optional[pd.DataFrame]:
    """
    Recebe uma lista de URLs de arquivos, baixa-os, e combina em um único DataFrame.
    """
    if not file_urls:
        print("[Data Collector] Nenhuma URL de arquivo fornecida.")
        return None

    print(f"[Data Collector] Baixando {len(file_urls)} arquivo(s)...")
    list_of_dfs: List[pd.DataFrame] = []

    for url in file_urls:
        print(f"Tentando baixar: {url}")
        try:
            response = requests.get(url, timeout=90)
            response.raise_for_status()

            # Determina o formato pelo final da URL
            if url.lower().endswith('.csv'):
                df = pd.read_csv(io.StringIO(response.text), sep=sep)
            elif url.lower().endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(response.content))
            else:
                print(f"Aviso: Formato de arquivo não suportado para {url}")
                continue
            
            list_of_dfs.append(df)
            print(f"Sucesso ao baixar e processar: {url.split('/')[-1]}")

        except Exception as e:
            print(f"Falha ao baixar ou processar {url}. Erro: {e}")
            
    if not list_of_dfs:
        print("Nenhum dado foi baixado com sucesso.")
        return None

    print("Combinando todos os DataFrames...")
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    print("Combinação concluída!")
    return combined_df