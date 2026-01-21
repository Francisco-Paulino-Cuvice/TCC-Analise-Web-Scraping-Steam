import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o CSV
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Remove a tag 'Singleplayer' de cada string da coluna 'tags'
df['tags'] = df['tags'].dropna().apply(
    lambda x: ', '.join([tag.strip() for tag in x.split(',') if tag.strip() != 'Singleplayer'])
)



#
# Tags mais populares por ano
#



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

# Para cada ano, pegar X mais populares
top_5_por_ano = (
    tags_por_ano
    .sort_values(['release_year', 'frequencia'], ascending=[True, False])
    .groupby('release_year')
    .head(5)
)

# Mostrar (ou salvar) o resultado
#print(top_5_por_ano)

# Gráfico com tags no eixo Y e colunas por ano
sns.catplot(
    data=top_5_por_ano,
    x='frequencia',
    y='tags_list',
    col='release_year',
    kind='bar',
    col_wrap=4,  # Altere para mais colunas por linha, se quiser
    height=4,
    sharex=False,
    sharey=False
)

plt.subplots_adjust(top=0.9)
plt.suptitle("Top 5 Tags por Ano de Lançamento", fontsize=16)
plt.show()