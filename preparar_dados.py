import pandas as pd
import glob
import os

arquivos_interesse = sorted(glob.glob(os.path.join("data", "*.csv")))

dfs = []

print("A carregar e filtrar ficheiros...")

for arquivo in arquivos_interesse:
    try:
        df = pd.read_csv(arquivo)
        
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        

        df_2026 = df[df['created_at'].dt.year == 2026]
        
        print(f"Arquivo: {arquivo} | Total: {len(df)} -> Mantidos (2026): {len(df_2026)}")
        
        dfs.append(df_2026)
    except Exception as e:
        print(f"Erro ao ler {arquivo}: {e}")

if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    
    df_final = df_final.drop_duplicates(subset=['uri'])
    
    nome_saida = "posts-bbb26.csv"
    df_final.to_csv(nome_saida, index=False)
    print(f"\nSUCESSO! Arquivo limpo gerado: {nome_saida}")
    print(f"Total de posts prontos para análise: {len(df_final)}")
else:
    print("Nenhum dado encontrado.")
