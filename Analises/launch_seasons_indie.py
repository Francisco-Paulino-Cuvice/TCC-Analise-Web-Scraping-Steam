import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Converter datas
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df = df.dropna(subset=['release_date'])

# Extrair mês
df['mes'] = df['release_date'].dt.month

# Filtrar apenas jogos com a tag "Indie"
df_indie = df[df['tags'].str.contains('Indie', case=False, na=False)]

# Contar lançamentos por mês
indie_por_mes = df_indie['mes'].value_counts().sort_index()

# Nomes dos meses
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Plotar gráfico
plt.figure(figsize=(10,6))
plt.bar(meses, indie_por_mes)
plt.title('Distribuição de Lançamentos de Jogos Indie por Mês')
plt.xlabel('Mês')
plt.ylabel('Número de Lançamentos Indie')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()
