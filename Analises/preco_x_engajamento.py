import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Carregar e preparar o dataset
# ==============================
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Converter colunas
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['total_reviews_number'] = pd.to_numeric(df['total_reviews_number'], errors='coerce')

# Filtrar valores válidos
df = df[(df['price'] >= 0) & (df['total_reviews_number'] > 0)]

# ==============================
# Criar faixas de preço
# ==============================
bins = [-1, 0, 30, 60, 120, float('inf')]
labels = ['Gratuito', 'Até R$30', 'R$30–60', 'R$60–120', 'Acima de R$120']
df['faixa_preco'] = pd.cut(df['price'], bins=bins, labels=labels)

# ==============================
# Calcular estatísticas por faixa
# ==============================
engajamento_medio = df.groupby('faixa_preco')['total_reviews_number'].median().reset_index()
engajamento_medio.columns = ['Faixa de Preço', 'Mediana de Avaliações']

# ==============================
# Plotar gráfico
# ==============================
plt.figure(figsize=(10,6))
bars = plt.bar(
    engajamento_medio['Faixa de Preço'],
    engajamento_medio['Mediana de Avaliações'],
    color=['#6AA84F', '#FFD966', '#F6B26B', '#E06666', '#8E7CC3']
)

# Adicionar rótulos acima das barras
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 100, f'{int(yval):,}', 
             ha='center', va='bottom', fontsize=10)

# Ajustar escala logarítmica (porque há grandes diferenças)
plt.yscale('log')

plt.title('Engajamento (Mediana de Avaliações) por Faixa de Preço', fontsize=14)
plt.xlabel('Faixa de Preço')
plt.ylabel('Mediana de Avaliações (escala logarítmica)')
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()
