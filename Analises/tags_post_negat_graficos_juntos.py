import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Carregar o CSV
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Remove as tags 'Singleplayer' e 'Indie'
df['tags'] = df['tags'].dropna().apply(
    lambda x: ', '.join([tag.strip() for tag in x.split(',') if tag.strip() not in ['Singleplayer', 'Indie']])
)

# Criar figura com 2 subplots lado a lado
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

#
# Gráfico 1: Tags comuns entre jogos com avaliações negativas
#
filtro_neg = df['total_reviews'].str.contains('Negative', na=False)
jogos_neg = df[filtro_neg].copy()

jogos_neg['tags_list'] = jogos_neg['tags'].dropna().apply(lambda x: [tag.strip() for tag in x.split(',')])
todas_tags_neg = jogos_neg['tags_list'].explode()
contagem_tags_neg = Counter(todas_tags_neg)
top_tags_neg = contagem_tags_neg.most_common(10)

tags_neg, freq_neg = zip(*top_tags_neg)
sns.barplot(x=freq_neg, y=tags_neg, ax=axs[0])
axs[1].set_yticklabels(tags_neg, fontsize=14)
axs[1].set_title("Top 10 Tags - Jogos com Avaliações Negativas", fontsize=14)
axs[1].set_xlabel("Frequência", fontsize=14)
axs[1].set_ylabel("Tag", fontsize=14)

#
# Gráfico 2: Tags comuns entre jogos com avaliações extremamente positivas
#
filtro_pos = df['total_reviews'].str.contains('Overwhelmingly Positive', na=False)
jogos_pos = df[filtro_pos].copy()

jogos_pos['tags_list'] = jogos_pos['tags'].dropna().apply(lambda x: [tag.strip() for tag in x.split(',')])
todas_tags_pos = jogos_pos['tags_list'].explode()
contagem_tags_pos = Counter(todas_tags_pos)
top_tags_pos = contagem_tags_pos.most_common(10)

tags_pos, freq_pos = zip(*top_tags_pos)
sns.barplot(x=freq_pos, y=tags_pos, ax=axs[1])
axs[0].set_yticklabels(tags_pos, fontsize=14)
axs[0].set_title("Top 10 Tags - Jogos com Avaliações Extremamente Positivas", fontsize=14)
axs[0].set_xlabel("Frequência", fontsize=14)
axs[0].set_ylabel("Tag", fontsize=14)

plt.tight_layout()
plt.show()
