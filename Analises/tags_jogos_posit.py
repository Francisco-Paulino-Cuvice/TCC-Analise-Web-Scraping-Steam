import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Carregar o CSV
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Remove a tag 'Singleplayer' de cada string da coluna 'tags'
df['tags'] = df['tags'].dropna().apply(
    lambda x: ', '.join([tag.strip() for tag in x.split(',') if tag.strip() != 'Singleplayer' and tag.strip() != 'Indie'])
)



#
# Tags comuns entre jogos com avaliações positivas
#



# Filtro dos jogos com avaliação positiva
filtro = df['total_reviews'].str.contains('Overwhelmingly Positive', na=False)
jogos_pos = df[filtro].copy()

# Converter a coluna 'tags' para listas (caso sejam strings separadas por vírgula)
jogos_pos['tags_list'] = jogos_pos['tags'].dropna().apply(lambda x: [tag.strip() for tag in x.split(',')])

# Explodir todas as listas em uma única série de tags
todas_tags = jogos_pos['tags_list'].explode()

# Contar frequência de cada tag única
contagem_tags = Counter(todas_tags)

# Top 10 tags únicas mais comuns
top_tags = contagem_tags.most_common(10)

# Exibir no terminal
for tag, qtd in top_tags:
    print(f"{tag}: {qtd}")

# Gráfico de barras
tags, frequencias = zip(*top_tags)
sns.barplot(x=frequencias, y=tags)
plt.title("Top 10 Tags entre jogos de avaliações extremamente positivas")
plt.xlabel("Frequência")
plt.ylabel("Tag")
plt.tight_layout()
plt.show()