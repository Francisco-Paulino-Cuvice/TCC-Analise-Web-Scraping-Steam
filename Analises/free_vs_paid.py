import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Carregar e preparar o dataset
# ==============================
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Converter data e preço
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Remover linhas com data inválida
df = df.dropna(subset=['release_date'])

# Extrair ano do lançamento
df['ano'] = df['release_date'].dt.year

# ==============================
# Classificar jogos como pagos ou gratuitos
# ==============================
df['tipo'] = df['price'].apply(lambda x: 'Gratuito' if x == 0 else 'Pago')

# ==============================
# Contar proporção por ano
# ==============================
contagem = df.groupby(['ano', 'tipo']).size().unstack(fill_value=0)
proporcao = contagem.div(contagem.sum(axis=1), axis=0) * 100

# ==============================
# Plotar gráfico
# ==============================
plt.figure(figsize=(10,6))
proporcao.plot(kind='bar', stacked=True, color=['#66bb6a', '#42a5f5'], ax=plt.gca())

plt.title('Evolução da Proporção de Jogos Pagos vs Gratuitos por Ano', fontsize=14)
plt.xlabel('Ano de Lançamento')
plt.ylabel('Proporção (%)')
plt.legend(title='Tipo de Jogo', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.show()
