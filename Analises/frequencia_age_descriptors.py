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
# Frequência de conteúdos que limitam idade
#



df['age_descriptors'] = df['age_descriptors'].fillna('Livre')
df['age_descriptors'] = df['age_descriptors'].replace({'N/A': 'Livre'})

# Tratar descrições compostas como categorias múltiplas
descritores = df['age_descriptors'].str.split(', ')
contagem_descritores = Counter([desc.strip() for lista in descritores for desc in lista if desc])

pd.Series(contagem_descritores).sort_values(ascending=False).head(15).plot(
    kind='barh', title='Frequência de conteúdos de classificação indicativa (Top 15)'
)
plt.xlabel('Número de Jogos')
plt.tight_layout()
plt.show()