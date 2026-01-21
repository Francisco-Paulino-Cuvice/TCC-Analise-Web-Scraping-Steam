import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import aiohttp
import csv
import os
import sys
import traceback
from datetime import datetime
import re

# CSV com os links
INPUT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "steam_games_all_definitivo.csv")

# CSV resultado
OUTPUT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "steam_games_detailed_definitivo.csv")

# Ano de partida
START_YEAR = 2015

def parse_release_date(date_str):
    for fmt in ('%d %b, %Y', '%b %d, %Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except Exception:
            continue
    return None

# Pega avaliacoes totais pela API da Steam
async def get_total_reviews_steam_api(app_id: str) -> str:
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1&filter=recent&language=all&purchase_type=all"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    summary = data.get("query_summary", {})
                    total = summary.get("total_reviews", None)
                    if total is not None:
                        return str(total)
    except Exception as e:
        print(f"❌ Erro ao obter total de reviews pela API para app_id {app_id}: {e}")
    return "N/A"

# Raspa as informacoes dos jogos
async def scrape_game_details(playwright, game):
    url = game['link']
    title = game['title']

    # Tenta coletar 3 vezes
    for attempt in range(1, 4):
        browser = None
        try:
            # Browser: Chromium headless
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(url, timeout=30000)

            # Verifica se foi redirecionado para página de login
            if "login" in page.url or "steamlogin" in page.url:
                print(f"🔐 Jogo requer login, pulando.")
                await browser.close()
                return None
            
            # Detecção de agecheck e preenchimento
            try:
                age_year_locator = page.locator("select#ageYear")
                await age_year_locator.wait_for(state="visible", timeout=2000)

                print("ℹ️ Agecheck detectado. Preenchendo formulário...")
                await page.locator("select#ageDay").select_option("1")
                # Usar o texto "January" é mais legível e igualmente válido ao valor "1"
                await page.locator("select#ageMonth").select_option("January") 
                await age_year_locator.select_option("1990")

                # Usar page.evaluate para executar o .click() diretamente no DOM é mais confiável.
                await page.evaluate("document.getElementById('view_product_page_btn').click();")

                print("✅ Agecheck enviado. Aguardando carregamento da página do jogo...")
                # Espera a página carregar após o clique. É mais confiável que um timeout fixo.
                await page.wait_for_load_state("domcontentloaded", timeout=10000)
                await page.wait_for_timeout(1000) # Pausa extra para garantir a renderização de JS

            except PlaywrightTimeoutError:
                # Se o seletor de idade não aparecer em 5 segundos, é seguro assumir que não há agecheck.
                pass
            except Exception as e:
                # Captura outros erros que possam ocorrer durante o processo do agecheck
                print(f"⚠️ Erro inesperado ao lidar com agecheck: {e}")

            # Análises totais (texto, tipo: "Muito positivas")
            total_reviews = "N/A"

            review_rows = await page.query_selector_all('.user_reviews_summary_row')

            if review_rows:
                # Usa a última (em geral, é a de "todas as análises")
                total_row = review_rows[-1]

                try:
                    # Primeiro tenta coletar a descrição com itemprop
                    score_el = await total_row.query_selector('[itemprop="description"]')
                    if score_el:
                        total_reviews = (await score_el.inner_text()).strip()
                    else:
                        score_el = await total_row.query_selector('span.game_review_summary')
                        if score_el:
                            total_reviews = (await score_el.inner_text()).strip()
                except:
                    pass


            # Número total de reviews via API Steam (usando o id do jogo)
            total_reviews_number = await get_total_reviews_steam_api(game['id'])

            # Tags
            tags = []
            tag_els = await page.query_selector_all('a.app_tag')
            for t in tag_els:
                tag_text = await t.inner_text()
                tags.append(tag_text.strip())
            tags_text = ", ".join(tags) if tags else "N/A"

            # Detalhes do jogo (ex: Um jogador, Multijogador, etc.)
            details_text = "N/A"
            details_list = []

            details_els = await page.query_selector_all('a.game_area_details_specs_ctn div.label')
            for detail_el in details_els:
                text = (await detail_el.inner_text()).strip()
                if text:
                    details_list.append(text)

            if details_list:
                details_text = ", ".join(details_list)


            # Preço sem promoção
            price = "N/A"

            # Tenta encontrar a div correta do jogo (e não da demo)
            purchase_blocks = await page.query_selector_all('div.game_area_purchase_game')
            for block in purchase_blocks:
                block_class = await block.get_attribute("class")
                if "demo_above_purchase" not in block_class:
                    price_el = await block.query_selector('div.game_purchase_price.price') or await block.query_selector('div.discount_original_price')
                    if price_el:
                        price = (await price_el.inner_text()).strip()
                        break  # achou o preço real, pode sair do loop


            # Número de DLCs
            dlc_count = 0
            dlc_section = await page.query_selector('#gameAreaDLCSection')
            if dlc_section:
                em_el = await dlc_section.query_selector('em')
                if em_el:
                    em_text = (await em_el.inner_text()).strip()
                    match = re.search(r'\((\d+)\)', em_text)
                    if match:
                        dlc_count = match.group(1)


            # Descritores da classificação indicativa (ex: Violence, Inappropriate Language)
            age_descriptors = "N/A"
            desc_el = await page.query_selector('p.descriptorText')
            if desc_el:
                desc_raw = await desc_el.inner_text()
                desc_lines = [line.strip() for line in desc_raw.split('\n') if line.strip()]
                if desc_lines:
                    age_descriptors = ", ".join(desc_lines)


            await browser.close()

            return {
                'id': game['id'],
                'title': title,
                'release_date': game['release_date'],
                'total_reviews': total_reviews,
                'total_reviews_number': total_reviews_number,
                'tags': tags_text,
                'details': details_text,
                'price': price,
                'dlc_count': dlc_count,
                'age_descriptors': age_descriptors,
                'link': url
            }

        except PlaywrightTimeoutError:
            print(f"⚠️ Timeout carregando {title} (tentativa {attempt}/3). Tentando novamente...")
        except Exception as e:
            print(f"⚠️ Erro ao coletar {title} (tentativa {attempt}/3): {e}")
            traceback.print_exc()
        finally:
            if browser:
                try:
                    await browser.close()
                except:
                    pass

    print(f"❌ Falha após 3 tentativas, pulando jogo: {title}")
    return None


async def main():
    try:
        with open(INPUT_CSV, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            games = [row for row in reader]
    except Exception as e:
        print("❌ Erro ao ler CSV de entrada:", e)
        sys.exit(1)

    # Filtrar antes da requisição
    now = datetime.now()
    filtered_games = []
    for g in games:
        rd_str = g.get('release_date', '')
        rd_obj = parse_release_date(rd_str)
        if rd_obj and rd_obj.year >= START_YEAR and rd_obj <= now:
            filtered_games.append(g)

    print(f"ℹ️ Jogos filtrados (2015 até hoje): {len(filtered_games)} de {len(games)}")

    all_results = []
    total_games = len(filtered_games)
    processed = 0
    saved = 0
    skipped = 0

    # Numero limite de jogos a coletar 
    # Sincronize com o numero de linhas no CSV de entrada
    # Ou coloque um limite para fazer em partes
    LIMIT = 48590
    idx = 0
    first_save = True  # Para controlar se o cabeçalho já foi escrito

    async with async_playwright() as playwright:
        for game in filtered_games[:LIMIT]:
            processed += 1
            print(f"🎮 [{processed}/{total_games}] Coletando: {game.get('title', 'Sem título')}")
            result = await scrape_game_details(playwright, game)

            if result:
                all_results.append(result)
            else:
                skipped += 1
                print(f"⚠️ Jogo ignorado ou falha na coleta")

            idx += 1

            # Salvar a cada 10 jogos iterados
            if idx % 10 == 0:
                try:
                    with open(OUTPUT_CSV, 'a', encoding='utf-8', newline='') as f_out:
                        fieldnames = ['id', 'title', 'release_date', 'total_reviews', 'total_reviews_number',
                                    'tags', 'details', 'price', 'dlc_count', 'age_descriptors', 'link']
                        writer = csv.DictWriter(f_out, fieldnames=fieldnames)

                        if first_save:
                            writer.writeheader()
                            first_save = False

                        writer.writerows(all_results)
                        saved += len(all_results)
                    print(f"💾 Backup salvo com {len(all_results)} jogos em {OUTPUT_CSV}. Total salvo: {saved}. Total ignorado: {skipped}")
                    all_results.clear()
                except Exception as e:
                    print("❌ Erro ao salvar CSV parcial:", e)

    # Salvar qualquer restante que não tenha sido salvo ainda
    if all_results:
        try:
            with open(OUTPUT_CSV, 'a', encoding='utf-8', newline='') as f_out:
                fieldnames = ['id', 'title', 'release_date', 'total_reviews', 'total_reviews_number',
                            'tags', 'details', 'price', 'dlc_count', 'age_descriptors', 'link']
                writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                if first_save:
                    writer.writeheader()
                writer.writerows(all_results)
                saved += len(all_results)
            print(f"\n✅ Dados finais salvos em {OUTPUT_CSV}. Total salvo: {saved}. Total ignorado: {skipped}")
        except Exception as e:
            print("❌ Erro ao salvar CSV final:", e)
if __name__ == "__main__":
    try:
        asyncio.run(main())
        print(f"\n✅ Coleta Salva e Finalizada.")
    except KeyboardInterrupt:
        print("\n🛑 Execução interrompida pelo usuário.")
    except Exception as e:
        print("❌ Erro inesperado:", e)
        traceback.print_exc()
