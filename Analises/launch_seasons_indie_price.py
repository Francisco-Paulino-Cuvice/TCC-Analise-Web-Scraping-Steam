import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Carregar o dataset
# ==============================
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Converter datas
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df = df.dropna(subset=['release_date'])

# Converter preço para número
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Extrair mês
df['mes'] = df['release_date'].dt.month

# ==============================
# Filtrar apenas jogos com a tag "Indie"
# ==============================
df_indie = df[df['tags'].str.contains('Indie', case=False, na=False)].copy()


#metricas precos
mediana_preco = df_indie['price'].median()
media_preco = df_indie['price'].mean()

print(f'mediana preco: R${mediana_preco:.2f}')
print(f'media preco: R${media_preco:.2f}')

# ==============================
# Definir faixas de preço
# ==============================
bins = [-1, 0, 20, 50, 80, float('inf')]
labels = ['Gratuito', 'Até R$20', 'R$20–50', 'R$50–80', 'Acima de R$80']
df_indie['faixa_preco'] = pd.cut(df_indie['price'], bins=bins, labels=labels)

# ==============================
# Contar lançamentos por mês e faixa de preço
# ==============================
tabela = df_indie.groupby(['mes', 'faixa_preco']).size().unstack(fill_value=0)

# Nomes dos meses
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
tabela.index = meses[:len(tabela)]

# ==============================
# Plotar gráfico
# ==============================
ax = tabela.plot(kind='bar', stacked=True, figsize=(12,7))

plt.title('Distribuição de Lançamentos de Jogos Indie por Faixa de Preço e Mês', fontsize=14)
plt.xlabel('Mês de Lançamento')
plt.ylabel('Número de Lançamentos')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.5)

# 🔹 Legenda à direita, fora do gráfico
plt.legend(
    title='Faixa de Preço',
    bbox_to_anchor=(1.02, 1),   # move pra fora, à direita
    loc='upper left',
    frameon=True
)

# Ajuste de layout pra não cortar nada
plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.show()
