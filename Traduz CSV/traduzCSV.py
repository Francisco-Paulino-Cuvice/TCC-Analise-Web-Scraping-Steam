import pandas as pd
import re

# 1. Defina o mapeamento de tradução (inglês: português) com VARIAÇÕES
translation_map = {
    # Corrigindo e adicionando variações de 'Third Person' e 'First Person'
    'Third-Person': 'Terceira Pessoa', 
    'Third Person': 'Terceira Pessoa',  # Sem hífen
    'Thirdperson': 'Terceira Pessoa',  # Sem espaço
    'Third-Person Shooter': 'Tiro em Terceira Pessoa', 
    'Third Person Shooter': 'Tiro em Terceira Pessoa', # Sem hífen
    
    'First-Person': 'Primeira Pessoa',
    'First Person': 'Primeira Pessoa',
    'Firstperson': 'Primeira Pessoa',
    
    'Shooter': 'Tiro', 
    'FPS': 'FPS (Tiro em Primeira Pessoa)', # Tradução explícita do acrônimo
    
    'Mod': 'Modificadores',
    'Games Workshop': 'Oficina de jogos',
    'Co-op': 'Cooperativo',
    'Online Co-op': 'Cooperativo Online',
    'Epic': 'Épico',
    'Competitive': 'Competitivo',
    'Team-Based': 'Baseado em times',
    'Open World Survival Craft': 'Sobrevivência em mundo aberto',
    'Horses': 'Cavalos',
    'Elf': 'Elfos',
    'Adventure': 'Aventura',
    'Action': 'Ação',
    'Casual': 'Casual',
    'Simulation': 'Simulação',
    'Atmospheric': 'Atmosférico',
    'Story Rich': 'Rico em história',
    'Multiplayer': 'Multijogador',
    'Strategy': 'Estratégia',
    'Exploration': 'Exploração',
    'Great Soundtrack': 'Boa trilha sonora',
    'Cute': 'Fofo',
    'Puzzle': 'Quebra-cabeça',
    'Pixel Graphics': 'Gráficos pixelados',
    'Early Access': 'Acesso Antecipado',
    'Open World': 'Mundo Aberto',
    'Fantasy': 'Fantasia',
    'Funny': 'Engraçado',
    'Difficult': 'Difícil',
    'Tactical': 'Tático',
    'Stealth': 'Furtivo',
    'In-game purchases': 'Compras no Jogo',
    'In-game chat': 'Conversas no Jogo',
    'Online interactivity': 'Interatividade Online',
    'Single-player': 'Um Jogador',
    'Family Sharing': 'Compartilhamento em Família',
    'Steam Achievements': 'Conquistas Steam',
    'Steam Cloud': 'Nuvem Steam',
    'Steam Trading Cards': 'Cartas de Trocas Steam',
    'Online PvP': 'PvP Online',
    'Steam Leaderboards': 'Placar Steam',
    'In-App Purchases': 'Compras no Aplicativo',
    'Remote Play on TV': 'Reprodução Remota na TV',
    'Steam Workshop': 'Oficina Steam',
    'Cross-Platform Multiplayer': 'Multijogador entre Plataformas',
    'Stats': 'Estatísticas',
    'Shared/Split Screen PvP': 'PvP com Tela Compartilhada/Dividida',
    # Outros termos
    'Souls-like': 'Souls-like',
    'MOBA': 'MOBA',
    'Dungeons & Dragons': 'Dungeons & Dragons',
    'Looter Shooter': 'Looter Shooter',
    'Battle Royale': 'Battle Royale',
    'Hero Shooter': 'Tiro de Heróis',
    'Extraction Shooter': 'Tiro de Extração',
    '2D': '2D',
    '3D': '3D',
    'RPG': 'RPG',
    'PvP': 'PvP',
    'Indie': 'Indie',
}

# 2. Limpeza e criação do mapa de tradução
translation_map_clean = {k.strip(): v for k, v in translation_map.items()}


# Função auxiliar para traduzir uma string de tags separadas por vírgula
def translate_csv_cell(cell_value):
    if pd.isna(cell_value):
        return cell_value

    # Divide a string em tags individuais, usando vírgula como separador
    tags = re.split(r',\s*', str(cell_value))

    # Tenta traduzir cada tag
    translated_tags = []
    for tag in tags:
        clean_tag = tag.strip()
        # Usa .get() para traduzir, se a chave não existir, retorna a tag original
        translated_tags.append(translation_map_clean.get(clean_tag, clean_tag))

    # Junta as tags traduzidas de volta em uma string separada por vírgula
    return ', '.join(translated_tags)


# 3. Carregar o arquivo CSV original
try:
    df = pd.read_csv('steam_games_detailed_limpo_menor.csv')

    # 4. Identificar as colunas que precisam de tradução interna
    # MANTER OU AJUSTAR AQUI CONFORME SEU CSV
    columns_to_translate = ['tags', 'details', 'age_descriptors'] 

    # 5. Iterar sobre as colunas e aplicar a função de tradução (SOBRESCREVENDO)
    for col in columns_to_translate:
        if col in df.columns:
            # Sobrescreve a coluna original com os valores traduzidos
            df[col] = df[col].apply(translate_csv_cell)
            print(f"✔️ Coluna '{col}' traduzida e sobrescrita com sucesso.")
        else:
            print(f"⚠️ Aviso: A coluna '{col}' não foi encontrada no arquivo CSV.")


    # 6. Salvar o novo DataFrame em um novo arquivo CSV
    output_filename = 'steam_games_detailed_limpo_menor_traduzido.csv'
    df.to_csv(output_filename, index=False)

    print(f"\n✅ Arquivo CSV traduzido criado com sucesso: '{output_filename}'")
    print("\nAs primeiras linhas das colunas traduzidas são:")
    # Exibe as primeiras linhas das colunas relevantes para confirmação
    print(df.filter(items=columns_to_translate).head())

except FileNotFoundError:
    print("❌ Erro: O arquivo 'steam_games_detailed_limpo_menor.csv' não foi encontrado.")
except Exception as e:
    print(f"❌ Ocorreu um erro durante o processamento: {e}")