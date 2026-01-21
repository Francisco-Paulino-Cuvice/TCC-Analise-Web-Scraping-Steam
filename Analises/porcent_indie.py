import pandas as pd

# Carregar o dataset
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Filtrar jogos com a tag "Indie"
indie_mask = df['tags'].str.contains('Indie', case=False, na=False)

# Calcular totais
total_jogos = len(df)
total_indie = indie_mask.sum()

# Calcular porcentagem
porcentagem_indie = (total_indie / total_jogos) * 100

print(f"Jogos Indie: {total_indie} de {total_jogos} ({porcentagem_indie:.2f}%)")