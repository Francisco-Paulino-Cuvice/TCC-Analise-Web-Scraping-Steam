import asyncio
from playwright.async_api import async_playwright
import csv
import os

# Endereco de busca da steam
BASE_URL = "https://store.steampowered.com/search/"

# Filtros aplicados: apenas jogos, ignorar preferencias, ordem alfabetica e numero da pagina (manipulado pelo script)
PARAMS = "?category1=998&ndl=1&ignore_preferences=1&sort_by=Name_ASC&page="

# Maximo de paginas que serão raspadas
# Cada pagina possui uma lista de 25 jogos
MAX_PAGES = 10

script_dir = os.path.dirname(os.path.abspath(__file__))

# Nome do arquivo a ser gerado com os dados raspados
OUTPUT_CSV = os.path.join(script_dir, "steam_games_temp.csv")

async def scrape_steam():
    async with async_playwright() as p:

        # Browser escolhido: Chromium headless
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Arquivo de registro
        all_games = []

        # Numero da pagina para comecar
        page_number = 1

        while page_number <= MAX_PAGES:
            url = BASE_URL + PARAMS + str(page_number)
            print(f"[Página {page_number}] Acessando: {url}")
            await page.goto(url)
            await page.wait_for_timeout(2000)
            
            # Localiza a lista de jogos
            game_elements = await page.query_selector_all('.search_result_row')

            # Se nao ha lista, para a raspagem
            if not game_elements:
                print("✅ Fim da listagem.")
                break

            # Para cada jogo na lista,  extrai os dados disponiveis e o link da pagina do jogo
            for el in game_elements:
                title_el = await el.query_selector('.title')
                title = await title_el.inner_text() if title_el else "Sem título"

                price_el = await el.query_selector('.discount_final_price') or await el.query_selector('.search_price')
                price = await price_el.inner_text() if price_el else "Gratuito ou Indefinido"

                link = await el.get_attribute('href')

                # Extrair ID do link
                game_id = ""
                if link:
                    parts = link.split('/')
                    if "app" in parts:
                        idx = parts.index("app")
                        if idx + 1 < len(parts):
                            game_id = parts[idx + 1]

                # Extrair data de lançamento
                release_el = await el.query_selector('.search_released')
                release_date = await release_el.inner_text() if release_el else "Indefinido"

                # Coloca no arquivo de registro
                all_games.append({
                    'id': game_id,
                    'title': title.strip(),
                    'price': price.strip(),
                    'release_date': release_date.strip(),
                    'link': link.strip() if link else ""
                })

            print(f"  → {len(game_elements)} jogos encontrados.")
            page_number += 1

        await browser.close()

        # Salvar CSV
        with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'title', 'price', 'release_date', 'link'])
            writer.writeheader()
            writer.writerows(all_games)

        print(f"\n💾 {len(all_games)} jogos salvos em {OUTPUT_CSV}")

if __name__ == "__main__":
    asyncio.run(scrape_steam())
