import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations

# Carregar o CSV
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Remove a tag 'Singleplayer' de cada string da coluna 'tags'
df['tags'] = df['tags'].dropna().apply(
    lambda x: ', '.join([tag.strip() for tag in x.split(',') if tag.strip() != 'Singleplayer'])
)



#
# Combinações frequentes de tags e impacto nas avaliações
#



# Preparar os dados
df['tags'] = df['tags'].fillna('')
df['tags_list'] = df['tags'].str.split(', ')

# Parâmetros
min_freq = 5      # Mínimo de vezes que uma combinação deve aparecer
max_comb = 3      # Tamanho máximo da combinação (2 ou 3 tags)

# Dicionários para armazenar frequência e soma de avaliações
comb_freq = defaultdict(int)
comb_sum_reviews = defaultdict(float)

# Iterar sobre os jogos e calcular combinações
for _, row in df.iterrows():
    tags = sorted(set(row['tags_list']))  # remover duplicadas e ordenar
    reviews = row['total_reviews_number']
    for r in range(2, max_comb+1):
        for comb in combinations(tags, r):
            comb_freq[comb] += 1
            comb_sum_reviews[comb] += reviews

# Calcular média de avaliações para combinações frequentes
dados_combinacoes = []
for comb, freq in comb_freq.items():
    if freq >= min_freq:
        media = comb_sum_reviews[comb] / freq
        dados_combinacoes.append({
            'combinacao': ', '.join(comb),
            'frequencia': freq,
            'media_avaliacoes': media
        })

# Criar DataFrame com os resultados
df_combs = pd.DataFrame(dados_combinacoes)
df_combs = df_combs.sort_values(by='media_avaliacoes', ascending=False)


# Mostrar as 15 combinações com maior média de avaliações
top_combs = df_combs.head(15)

# Criar o gráfico de barras horizontais
plt.figure(figsize=(12, 8)) # Ajuste o tamanho para melhor visualização
plt.barh(top_combs['combinacao'], top_combs['media_avaliacoes'], color='skyblue')
plt.xlabel('Média de Avaliações por Jogo (em milhões)')
plt.ylabel('Combinação de Tags')
plt.title('Top 15 Combinações de Tags com Maior Média de Avaliações')
plt.gca().invert_yaxis() # Inverte o eixo Y para a maior barra ficar no topo
plt.tight_layout() # Ajusta o layout para evitar sobreposição
plt.show()