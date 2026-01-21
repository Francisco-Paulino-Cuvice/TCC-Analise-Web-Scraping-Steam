import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# Carregar o CSV
# ==============================
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# ==============================
# Limpeza das tags
# ==============================
# Remove a tag 'Singleplayer' de cada string da coluna 'tags'
df['tags'] = df['tags'].dropna().apply(
    lambda x: ', '.join([tag.strip() for tag in x.split(',') if tag.strip() != 'Singleplayer'])
)

# ==============================
# Preparação por ano
# ==============================
# Converter release_date para datetime
df['release_date'] = pd.to_datetime(df['release_date'], format='%d %b, %Y', errors='coerce')

# Extrair o ano
df['release_year'] = df['release_date'].dt.year

# Converter tags em lista
df['tags_list'] = df['tags'].dropna().apply(lambda x: [tag.strip() for tag in x.split(',')])

# Explodir as tags
df_explodido = df.explode('tags_list')

# Agrupar por ano e tag, contando frequência
tags_por_ano = (
    df_explodido
    .groupby(['release_year', 'tags_list'])
    .size()
    .reset_index(name='frequencia')
)

# Para cada ano, pegar as 10 tags mais populares
top_por_ano = (
    tags_por_ano
    .sort_values(['release_year', 'frequencia'], ascending=[True, False])
    .groupby('release_year')
    .head(10)
)

# ==============================
# Heatmap único
# ==============================
# Pivotar os dados para formato adequado para heatmap
pivot = top_por_ano.pivot_table(
    index='tags_list',       # Eixo Y = tags
    columns='release_year',  # Eixo X = anos
    values='frequencia',     # Valor = frequência
    fill_value=0             # Preenche com 0 onde não houver valor
)

# Converter para inteiro para evitar erro de formatação no heatmap
pivot = pivot.astype(int)

# Ordenar tags por frequência total (opcional, para destacar mais populares)
tags_ordenadas = pivot.sum(axis=1).sort_values(ascending=False).index
pivot = pivot.loc[tags_ordenadas]

# Plotar heatmap
plt.figure(figsize=(12, 7))  # tamanho menor
sns.heatmap(
    pivot,
    annot=False,  # remove números para limpar visualmente
    cmap="YlGnBu",
    cbar_kws={'label': 'Frequência'}
)
plt.title("Frequência das Top Tags por Ano", fontsize=14)
plt.xlabel("Ano", fontsize=12)
plt.ylabel("Tags", fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
