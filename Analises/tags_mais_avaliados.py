import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Carregar o CSV
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Remove a tag 'Singleplayer' de cada string da coluna 'tags'
df['tags'] = df['tags'].dropna().apply(
    lambda x: ', '.join([tag.strip() for tag in x.split(',') if tag.strip() != 'Singleplayer'])
)



#
# Tags mais frequentes entre os jogos mais avaliados
#



# Definir quantos jogos do topo usar
top_n = 500# int(0.05 * len(df))

# Selecionar os jogos com mais avaliações
jogos_top = df.sort_values(by='total_reviews_number', ascending=False).head(top_n).copy()

# Quebrar e contar as tags dos jogos mais avaliados
jogos_top['tags'] = jogos_top['tags'].fillna('')
tags_top = jogos_top['tags'].str.split(', ')
contagem_tags_top = Counter([tag for lista in tags_top for tag in lista if tag])

# Exibir as tags mais frequentes nesses jogos
pd.Series(contagem_tags_top).sort_values(ascending=False).head(20).plot(
    kind='barh', figsize=(10, 6), title=f'Tags mais comuns entre os {top_n} jogos com mais avaliações'
)
plt.xlabel('Número de Jogos com a Tag')
plt.tight_layout()
plt.show()

# Mostrar os dados
pd.Series(contagem_tags_top).sort_values(ascending=False).head(20)