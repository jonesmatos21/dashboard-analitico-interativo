import pandas as pd
import numpy as np

np.random.seed(42)

estados_dados = [
    # Região Norte
    {"Estado": "AC", "Regiao": "Norte", "Taxa_Analfabetismo": 8.4, "Total_Criancas": 85000, "Criancas_Nao_Alfabetizadas": 7140},
    {"Estado": "AP", "Regiao": "Norte", "Taxa_Analfabetismo": 9.1, "Total_Criancas": 92000, "Criancas_Nao_Alfabetizadas": 8372},
    {"Estado": "AM", "Regiao": "Norte", "Taxa_Analfabetismo": 10.5, "Total_Criancas": 450000, "Criancas_Nao_Alfabetizadas": 47250},
    {"Estado": "PA", "Regiao": "Norte", "Taxa_Analfabetismo": 11.2, "Total_Criancas": 890000, "Criancas_Nao_Alfabetizadas": 99680},
    {"Estado": "RO", "Regiao": "Norte", "Taxa_Analfabetismo": 6.8, "Total_Criancas": 180000, "Criancas_Nao_Alfabetizadas": 12240},
    {"Estado": "RR", "Regiao": "Norte", "Taxa_Analfabetismo": 9.8, "Total_Criancas": 75000, "Criancas_Nao_Alfabetizadas": 7350},
    {"Estado": "TO", "Regiao": "Norte", "Taxa_Analfabetismo": 7.5, "Total_Criancas": 160000, "Criancas_Nao_Alfabetizadas": 12000},

    # Região Nordeste
    {"Estado": "AL", "Regiao": "Nordeste", "Taxa_Analfabetismo": 12.4, "Total_Criancas": 350000, "Criancas_Nao_Alfabetizadas": 43400},
    {"Estado": "BA", "Regiao": "Nordeste", "Taxa_Analfabetismo": 11.8, "Total_Criancas": 1500000, "Criancas_Nao_Alfabetizadas": 177000},
    {"Estado": "CE", "Regiao": "Nordeste", "Taxa_Analfabetismo": 8.1, "Total_Criancas": 980000, "Criancas_Nao_Alfabetizadas": 79380},
    {"Estado": "MA", "Regiao": "Nordeste", "Taxa_Analfabetismo": 13.5, "Total_Criancas": 820000, "Criancas_Nao_Alfabetizadas": 110700},
    {"Estado": "PB", "Regiao": "Nordeste", "Taxa_Analfabetismo": 9.6, "Total_Criancas": 400000, "Criancas_Nao_Alfabetizadas": 38400},
    {"Estado": "PE", "Regiao": "Nordeste", "Taxa_Analfabetismo": 10.2, "Total_Criancas": 950000, "Criancas_Nao_Alfabetizadas": 96900},
    {"Estado": "PI", "Regiao": "Nordeste", "Taxa_Analfabetismo": 11.0, "Total_Criancas": 360000, "Criancas_Nao_Alfabetizadas": 39600},
    {"Estado": "RN", "Regiao": "Nordeste", "Taxa_Analfabetismo": 9.3, "Total_Criancas": 380000, "Criancas_Nao_Alfabetizadas": 35340},
    {"Estado": "SE", "Regiao": "Nordeste", "Taxa_Analfabetismo": 9.9, "Total_Criancas": 250000, "Criancas_Nao_Alfabetizadas": 24750},

    # Região Centro-Oeste
    {"Estado": "DF", "Regiao": "Centro-Oeste", "Taxa_Analfabetismo": 3.2, "Total_Criancas": 320000, "Criancas_Nao_Alfabetizadas": 10240},
    {"Estado": "GO", "Regiao": "Centro-Oeste", "Taxa_Analfabetismo": 5.1, "Total_Criancas": 720000, "Criancas_Nao_Alfabetizadas": 36720},
    {"Estado": "MT", "Regiao": "Centro-Oeste", "Taxa_Analfabetismo": 5.9, "Total_Criancas": 410000, "Criancas_Nao_Alfabetizadas": 24190},
    {"Estado": "MS", "Regiao": "Centro-Oeste", "Taxa_Analfabetismo": 4.8, "Total_Criancas": 300000, "Criancas_Nao_Alfabetizadas": 14400},

    # Região Sudeste
    {"Estado": "ES", "Regiao": "Sudeste", "Taxa_Analfabetismo": 4.1, "Total_Criancas": 450000, "Criancas_Nao_Alfabetizadas": 18450},
    {"Estado": "MG", "Regiao": "Sudeste", "Taxa_Analfabetismo": 5.0, "Total_Criancas": 2200000, "Criancas_Nao_Alfabetizadas": 110000},
    {"Estado": "RJ", "Regiao": "Sudeste", "Taxa_Analfabetismo": 5.5, "Total_Criancas": 1900000, "Criancas_Nao_Alfabetizadas": 104500},
    {"Estado": "SP", "Regiao": "Sudeste", "Taxa_Analfabetismo": 3.5, "Total_Criancas": 5100000, "Criancas_Nao_Alfabetizadas": 178500},

    # Região Sul
    {"Estado": "PR", "Regiao": "Sul", "Taxa_Analfabetismo": 3.8, "Total_Criancas": 1300000, "Criancas_Nao_Alfabetizadas": 49400},
    {"Estado": "RS", "Regiao": "Sul", "Taxa_Analfabetismo": 4.0, "Total_Criancas": 1200000, "Criancas_Nao_Alfabetizadas": 48000},
    {"Estado": "SC", "Regiao": "Sul", "Taxa_Analfabetismo": 3.1, "Total_Criancas": 850000, "Criancas_Nao_Alfabetizadas": 26350},
]

# Expand into a detailed dataset with categories like Localizacao (Urbana/Rural) and Faixa Etaria (6-8 anos, 9-11 anos, 12-14 anos)
rows = []
for item in estados_dados:
    for local in ["Urbana", "Rural"]:
        for faixa in ["6 a 8 anos", "9 a 11 anos", "12 a 14 anos"]:
            # Adjust rate based on local and faixa
            mult_local = 1.6 if local == "Rural" else 0.85
            mult_faixa = 1.4 if faixa == "6 a 8 anos" else (1.0 if faixa == "9 a 11 anos" else 0.7)
            taxa_adj = round(min(max(item["Taxa_Analfabetismo"] * mult_local * mult_faixa * np.random.uniform(0.9, 1.1), 1.0), 35.0), 2)

            total_sub = int(item["Total_Criancas"] * 0.16)
            nao_alf_sub = int(total_sub * (taxa_adj / 100.0))

            rows.append({
                "Estado": item["Estado"],
                "Regiao": item["Regiao"],
                "Localizacao": local,
                "Faixa_Etaria": faixa,
                "Taxa_Analfabetismo": taxa_adj,
                "Total_Criancas": total_sub,
                "Criancas_Nao_Alfabetizadas": nao_alf_sub,
                "Ano": 2025
            })

df_final = pd.DataFrame(rows)
df_final.to_csv("data/analfabetismo_infantil_2025.csv", index=False)
print("Dataset de analfabetismo infantil 2025 gerado com sucesso em data/analfabetismo_infantil_2025.csv")
