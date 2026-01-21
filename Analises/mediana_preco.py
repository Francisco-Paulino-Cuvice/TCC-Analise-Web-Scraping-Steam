import pandas as pd

# Carregar o dataset
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Converter a coluna de preço para numérica (caso contenha textos ou valores ausentes)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Remover valores ausentes
df = df.dropna(subset=['price'])

# Calcular a mediana
mediana_preco = df['price'].median()

media_preco = df['price'].mean()

maior_preco = df['price'].max()

df_pagos = df[df['price'] > 0]

# Calcular menor preço pago
menor_preco = df_pagos['price'].min()

print(f"Mediana do preço: R${mediana_preco:.2f}")
print(f"Media do preço: R${media_preco:.2f}")
print(f"Menor preço: R${menor_preco:.2f}")
print(f"Maior preço: R${maior_preco:.2f}")