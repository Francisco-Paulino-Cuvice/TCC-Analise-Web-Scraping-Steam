import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Carregar e preparar o dataset
# ==============================
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Converter data e garantir tipo numérico
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df = df.dropna(subset=['release_date', 'price'])

# Extrair o mês do lançamento
df['mes'] = df['release_date'].dt.month

# ==============================
# Definir as novas faixas de preço
# ==============================
bins = [-0.01, 0, 30, 60, 120, float('inf')]
labels = ['Gratuito', 'Até R$30', 'R$30-60', 'R$60-120', 'Acima de R$120']
df['faixa_preco'] = pd.cut(df['price'], bins=bins, labels=labels)

# ==============================
# Contagem por mês e faixa
# ==============================
lancamentos = df.groupby(['mes', 'faixa_preco']).size().unstack(fill_value=0)

# ==============================
# Plotar gráfico (somente UMA figura)
# ==============================
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

plt.figure(figsize=(10,6))
plt.bar(meses, lancamentos.sum(axis=1), color='lightgray', alpha=0.3)  # base opcional
lancamentos.reindex(range(1,13)).plot(
    kind='bar', stacked=True, figsize=(10,6), ax=plt.gca()
)

plt.title('Distribuição de Lançamentos por Faixa de Preço e Mês', fontsize=14)
plt.xlabel('Mês de Lançamento')
plt.ylabel('Número de Jogos')
plt.xticks(range(0,12), meses, rotation=0)

# 🔹 Legenda à direita, fora do gráfico
plt.legend(
    title='Faixa de Preço',
    bbox_to_anchor=(1.02, 1),   # desloca para a direita
    loc='upper left',
    frameon=True
)

plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout(rect=[0, 0, 0.85, 1])  # deixa espaço à direita pra legenda
plt.show()
