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
# Tags mais populares
#



# Quebrar tags e contar frequência
df['tags'] = df['tags'].fillna('')
tags_split = df['tags'].str.split(', ')
contagem_tags = Counter([tag for lista in tags_split for tag in lista if tag])

# Mostrar as 20 mais comuns
pd.Series(contagem_tags).sort_values(ascending=False).head(20).plot(
    kind='barh', figsize=(10, 6), title='Top 20 Tags mais comuns'
)
plt.xlabel('Número de Jogos')
plt.tight_layout()
plt.show()