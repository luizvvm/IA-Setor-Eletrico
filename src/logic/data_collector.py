# src/logic/data_collector.py
import pandas as pd
import requests
import io
from typing import List, Optional

BASE_URL = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/{dataset_slug}/{file_prefix}_{year}.{extension}"

def fetch_and_combine_data(
    dataset_slug: str,
    file_prefix: str,
    start_year: int,
    end_year: int,
    extension: str = 'csv',
    sep: str = ';'
) -> Optional[pd.DataFrame]:
    
    print(f"Iniciando busca do dataset '{dataset_slug}' de {start_year} até {end_year}...")
    list_of_dfs: List[pd.DataFrame] = []

    for year in range(start_year, end_year + 1):
        file_url = BASE_URL.format(
            dataset_slug=dataset_slug,
            file_prefix=file_prefix,
            year=year,
            extension=extension
        )
        print(f"Tentando baixar: {file_url}")
        try:
            response = requests.get(file_url, timeout=90)
            response.raise_for_status()
            
            df = pd.read_csv(io.StringIO(response.text), sep=sep, decimal=',')
            list_of_dfs.append(df)
            print(f"Sucesso ao baixar e processar dados de {year}.")
        except Exception as e:
            print(f"Aviso: Falha ao baixar ou processar o ano {year}. Erro: {e}")

    if not list_of_dfs:
        print("Nenhum dado foi baixado.")
        return None

    print("Combinando todos os DataFrames...")
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    print("Combinação concluída!")
    return combined_df