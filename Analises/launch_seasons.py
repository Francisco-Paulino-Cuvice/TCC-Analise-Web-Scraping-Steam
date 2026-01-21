import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Converter a data de lançamento
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Remover linhas sem data válida
df = df.dropna(subset=['release_date'])

# Extrair mês e ano
df['mes'] = df['release_date'].dt.month
df['ano'] = df['release_date'].dt.year

# Contar lançamentos por mês
lanc_por_mes = df['mes'].value_counts().sort_index()

# Nomes dos meses em português
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Plotar gráfico
plt.figure(figsize=(10,6))
plt.bar(meses, lanc_por_mes)
plt.title('Distribuição de Lançamentos por Mês na Steam')
plt.xlabel('Mês')
plt.ylabel('Número de Jogos Lançados')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()
