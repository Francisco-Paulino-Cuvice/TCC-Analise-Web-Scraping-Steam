import pandas as pd
import matplotlib.pyplot as plt
import re

# Carregar o CSV
df = pd.read_csv('../CSVs/Detalhes jogos 2015+/Detalhes limpos/steam_games_detailed_limpo_menor_traduzido.csv')

# Remove a tag 'Singleplayer' de cada string da coluna 'tags'
df['tags'] = df['tags'].dropna().apply(
    lambda x: ', '.join([tag.strip() for tag in x.split(',') if tag.strip() != 'Singleplayer'])
)



#
# Percentual de presença de funcionalidades
#



# Garantir que a coluna 'details' não tenha valores nulos para evitar erros.
df['details'] = df['details'].fillna('')

# Extrair todas as tags de detalhes únicas
all_details = set()
for detail_string in df['details']:
    # Dividir a string por vírgula e limpar espaços em branco
    details_list = [d.strip() for d in detail_string.split(',') if d.strip()]
    all_details.update(details_list)

# Converter o set de detalhes únicos para uma lista e ordenar para consistência
all_details_list = sorted(list(all_details))

# Criar colunas booleanas para cada detalhe
# Um dicionário para armazenar as séries booleanas
detail_presence = {}
for detail in all_details_list:
    # Usamos re.escape para garantir que caracteres especiais no detalhe (como parênteses)
    # sejam tratados literalmente na regex.
    detail_presence[detail] = df['details'].str.contains(re.escape(detail), case=False, na=False)

# Criar um DataFrame a partir do dicionário de séries booleanas
df_details_presence = pd.DataFrame(detail_presence)

# Calcular o percentual de presença para cada detalhe
percent_presence = (df_details_presence.mean() * 100).sort_values(ascending=False)

top_15_percent_presence = percent_presence.head(15)

# Exibir o percentual de presença
#print("🎮 Percentual de jogos com cada funcionalidade:")
#print(percent_presence.round(2))

# Visualização
plt.figure(figsize=(12, max(6, len(top_15_percent_presence) * 0.4))) # Tamanho ajustável dinamicamente
top_15_percent_presence.sort_values(ascending=True).plot(
    kind='barh',
    title='Presença de Funcionalidades nos Jogos'
)
plt.xlabel('Percentual (%)')
plt.ylabel('Funcionalidade')
plt.gca().tick_params(axis='y', labelsize=10) # Ajusta o tamanho da fonte dos rótulos do Y
plt.tight_layout()
plt.show()