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
# Jogos mais avaliados com avaliações extremamente positivas
#



# Filtro para jogos com avaliação "Overwhelmingly Positive" ("Extremamente positivas" em português)
filtro = df['total_reviews'].str.contains('Overwhelmingly Positive', na=False)

# Filtra e ordena pelos mais avaliados
jogos_extremely_positive = df[filtro].sort_values(by='total_reviews_number', ascending=False)

# Mostra os top 10
#print(jogos_extremely_positive[['title', 'total_reviews', 'total_reviews_number']].head(10))

top_jogos = jogos_extremely_positive.head(10)
sns.barplot(data=top_jogos, x='total_reviews_number', y='title')
plt.title("Top 10 jogos com avaliações Extremamente Positivas")
plt.xlabel("Número total de avaliações")
plt.ylabel("Nome do Jogo")
plt.show()