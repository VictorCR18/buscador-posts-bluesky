import pandas as pd
import glob
import os

# 1. Lista dos arquivos que queres no teu grafo de rivalidade
# Estou a usar os arquivos de "Team" e "Fora" e menções diretas dos dois rivais
arquivos_interesse = [
    "data/search_results_#ForaBabu_2026_01_20.csv",
    "data/search_results_#TeamAnaPaula_2026_01_20.csv",
    "data/search_results_#TeamBabu_2026_01_20.csv",
    "data/search_results_Ana Paula BBB_2026_01_20.csv",
    "data/search_results_Babu BBB_2026_01_20.csv",
    "data/search_results_Edilson capetinha BBB_2026_01_20.csv",
    "data/search_results_ForaAnaPaula_2026_01_20.csv",
]

dfs = []

print("A carregar e filtrar ficheiros...")

for arquivo in arquivos_interesse:
    try:
        df = pd.read_csv(arquivo)
        
        # Converter a coluna de data para datetime
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        
        # FILTRO CRÍTICO: Manter apenas posts de 2026
        # Removemos o "lixo" de 2016 e 2020 aqui
        df_2026 = df[df['created_at'].dt.year == 2026]
        
        print(f"Arquivo: {arquivo} | Total: {len(df)} -> Mantidos (2026): {len(df_2026)}")
        
        dfs.append(df_2026)
    except Exception as e:
        print(f"Erro ao ler {arquivo}: {e}")

# 2. Juntar tudo num único "Dataset da Treta"
if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    
    # Remover duplicatas (caso o mesmo post apareça em buscas diferentes)
    df_final = df_final.drop_duplicates(subset=['uri'])
    
    nome_saida = "posts-bbb26-rivalidades-filtrados.csv"
    df_final.to_csv(nome_saida, index=False)
    print(f"\nSUCESSO! Arquivo limpo gerado: {nome_saida}")
    print(f"Total de posts prontos para análise: {len(df_final)}")
else:
    print("Nenhum dado encontrado.")