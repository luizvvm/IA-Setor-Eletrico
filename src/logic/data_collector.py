# src/logic/data_collector.py

import pandas as pd
import requests
import io
from typing import List, Optional

# URL base genérica
BASE_URL = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/{dataset_slug}/{file_prefix}{date_part}.{extension}"

def fetch_and_combine_data(
    dataset_slug: str,
    file_prefix: str,
    start_year: int,
    end_year: int,
    extension: str = 'csv',
    frequency: str = 'yearly',
    start_month: int = 1,
    end_month: int = 12,
    sep: str = ';'
) -> Optional[pd.DataFrame]:
    
    print(f"Iniciando busca do dataset ({frequency}) '{dataset_slug}' de {start_month}/{start_year} até {end_month}/{end_year}...")
    list_of_dfs: List[pd.DataFrame] = []

    # Loop principal por anos
    for year in range(start_year, end_year + 1):
        if frequency == 'monthly':
            # LÓGICA CORRETA PARA ARQUIVOS MENSAIS
            s_month = start_month if year == start_year else 1
            e_month = end_month if year == end_year else 12
            for month_num in range(s_month, e_month + 1):
                month = f"{month_num:02d}"
                date_part = f"_{year}_{month}"
                file_url = BASE_URL.format(dataset_slug=dataset_slug, file_prefix=file_prefix, date_part=date_part, extension=extension)
                print(f"Tentando baixar: {file_url}")
                try:
                    response = requests.get(file_url, timeout=30)
                    response.raise_for_status()
                    if extension == 'csv':
                        df = pd.read_csv(io.StringIO(response.text), sep=sep)
                    else: # Assume xlsx
                        df = pd.read_excel(io.BytesIO(response.content))
                    list_of_dfs.append(df)
                    print(f"Sucesso ao baixar dados de {month}/{year}.")
                except requests.exceptions.HTTPError as e:
                    print(f"Aviso: Não foi possível baixar dados para {month}/{year}. Erro: {e}")
                except Exception as e:
                    print(f"Erro inesperado ao processar {month}/{year}. Erro: {e}")
        else: # frequency == 'yearly'
            # LÓGICA CORRETA PARA ARQUIVOS ANUAIS
            date_part = f"_{year}"
            file_url = BASE_URL.format(dataset_slug=dataset_slug, file_prefix=file_prefix, date_part=date_part, extension=extension)
            print(f"Tentando baixar: {file_url}")
            try:
                response = requests.get(file_url, timeout=60)
                response.raise_for_status()
                df = pd.read_csv(io.StringIO(response.text), sep=sep)
                list_of_dfs.append(df)
                print(f"Sucesso ao baixar dados de {year}.")
            except requests.exceptions.HTTPError as e:
                print(f"Aviso: Não foi possível baixar dados para {year}. Erro: {e}")
            except Exception as e:
                print(f"Erro inesperado ao processar {year}. Erro: {e}")

    if not list_of_dfs:
        print("Nenhum dado foi baixado.")
        return None

    print("Combinando todos os DataFrames...")
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    print("Combinação concluída!")
    return combined_df