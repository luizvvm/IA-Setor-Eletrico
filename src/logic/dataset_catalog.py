# src/logic/dataset_catalog.py

# Nosso catálogo agora tem um único dataset, tornando a IA especialista no assunto.
CURATED_DATASETS = [
    {
        "id": "indicadores-disponibilidade-geracao",
        "title": "Indicadores de Disponibilidade de Função Geração por Unidade Geradora",
        "notes": "Contém indicadores mensais, consolidados em arquivos anuais, sobre o desempenho e a disponibilidade das usinas geradoras do sistema. Ideal para analisar a confiabilidade e performance das usinas.",
        "slug": "ind_disponibilidade_fgeracao_uge_me",
        "file_prefix": "IND_DISPONIBILIDADE_FCGERACAO_UGE_MENSAL",
        "frequency": "yearly", # Um arquivo por ano
        "extension": "csv",
        "key_columns": ["nom_usina", "nom_unidade_geradora", "val_disponibilidade_apurada"]
    }
]