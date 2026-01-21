import pandas as pd
import matplotlib.pyplot as plt

# Carregar o CSV
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Remove a tag 'Singleplayer' de cada string da coluna 'tags'
df['tags'] = df['tags'].dropna().apply(
    lambda x: ', '.join([tag.strip() for tag in x.split(',') if tag.strip() != 'Singleplayer'])
)



#
# Média de avaliações por tag
#



# Garantir que tags estejam separadas e preenchidas
df['tags'] = df['tags'].fillna('')
tags_expandidas = df[['tags', 'total_reviews_number']].copy()
tags_expandidas['tags'] = tags_expandidas['tags'].str.split(', ')

# Explodir as tags para uma linha por tag
tags_explodidas = tags_expandidas.explode('tags')

# Calcular a média de avaliações por tag
media_avaliacoes_por_tag = tags_explodidas.groupby('tags')['total_reviews_number'].mean().sort_values(ascending=False)

# Mostrar as 20 tags com maior média
media_avaliacoes_por_tag.head(20).plot(kind='barh', figsize=(10, 6), title='Top 20 Tags com Maior Média de Avaliações por Jogo')
plt.xlabel('Média de Avaliações por Jogo')
plt.tight_layout()
plt.show()

# Exibir valores
media_avaliacoes_por_tag.head(20)