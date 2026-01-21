# Análise do mercado de jogos digitais via raspagem de dados da plataforma Steam

![GitHub repo size](https://img.shields.io/github/repo-size/Francisco-Paulino-Cuvice/TCC-Analise-Web-Scraping-Steam?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/Francisco-Paulino-Cuvice/TCC-Analise-Web-Scraping-Steam?style=for-the-badge)

> Arquivos e scripts Python utilizados no desenvolvimento do meu TCC de título "Análise do mercado de jogos digitais via raspagem de dados da plataforma Steam, visando auxiliar desenvolvedores na compreensão e inserção no mercado"

## 💻 Pré-requisitos

Antes de começar, verifique se você possui os seguintes requisitos:

- Linguagem `Python <3.11.9 ou maior>`.
- Sistema operacional `Windows`.
- Bibliotecas Python `Playwright`, `Matplotlib`, `Seaborn`, `Pandas`, `Numpy`.
- Navegador `Chromium` ou outro suportado pela `Playwright`.

## 🚀 Instalando o trabalho

Para instalar o trabalho, basta fazer download e descompactar o arquivo.

## ☕ Como usar

### Raspar lista de jogos da Steam

Na pasta `/Scraping/Raspagem lista de jogos`, abra o script `steam_games_limited.py` e configure como desejado. Ao executar, começará a raspagem da lista dos jogos da Steam. <br><br>
Ao final da raspagem, haverá um arquivo CSV com os resultados, que pode ser usado pelo próximo script para raspar os detalhes de cada jogo.

### Raspar lista de jogos da Steam
Na pasta `/Scraping/Raspagem detalhes jogos 2015+` há o script `steam_games_details_limited.py` e o CSV usado no TCC como template, que pode ser substituído colocando seu próprio CSV gerado pelo script `steam_games_limited.py`. 
Abra o script `steam_games_details_limited.py` e configure como desejado. <br><br>
Ao executar, esse script usa dos dados e links contidos no CSV de entrada para raspar detalhes dos jogos diretamente de suas páginas da Steam. <br><br>
Ao final da raspagem, haverá um arquivo CSV com os detalhes dos jogos contidos no CSV de entrada. É importante lembrar que os dados podem vir com inconsistências, então tente tratar valores nulos ou outros possíveis erros após a raspagem.

### Traduzir CSV
Na pasta `/Traduz CSV` está um script que traduz CSVs gerados pelo script `steam_games_details_limited.py` e um CSV template que pode ser substituído pelo seu próprio. <br><br>
O script possui um mapa de tradução que pode ser configurado como desejado.

### Análises
Na pasta `/Analises` estão os scripts que executam análises estatísticas de CSVs gerados pelo script `steam_games_details_limited.py`. <br><br>
Por padrão, o CSV das análises é o `steam_games_detailed_limpo_menor_traduzido.csv`.
Se deseja usar outro CSV, basta alterar o path na análise para o CSV desejado. Em sua maioria, os scripts geram gráficos estatísticos sobre o CSV de entrada.

### Documentos
na pasta `/Documentos` estão os textos relacionados ao trabalho.
- O PDF do TCC.
- Os PDFs do Resumo Expandido e Poster apresentado na 17° JOSIF em 2025 no IFSULDEMINAS - Campus Passos.
