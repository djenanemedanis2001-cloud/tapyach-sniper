import os
import sys
os.environ["PYTHONUNBUFFERED"] = "1"

from playwright.sync_api import sync_playwright
import time
import random

def log(message):
    print(message, flush=True)

class StoreBot:
    def __init__(self, csv_file="data.csv"):
        pass

    def get_user_data(self, count):
        users = []
        prenoms = ["Mohamed", "Amine", "Yacine", "Karim", "Sofiane", "Walid", "Ayoub", "Hamza", "Tarek", "Zaki"]
        noms = ["Saidi", "Benali", "Toumi", "Dahmani", "Zergui", "Mansouri", "Bouzid", "Haddad", "Slimani"]
        
        for i in range(count):
            nom_complet = f"{random.choice(prenoms)} {random.choice(noms)}"
            users.append({
                "nom": nom_complet,
                "telephone": f"055{random.randint(1000000, 9999999)}",
                "adresse_generique": f"Cite Test {random.randint(1, 100)}, Alger"
            })
        return users

    def execute_stress_test(self, url, max_orders=1):
        users = self.get_user_data(max_orders)
        if not users: return

        log(f"\n🚀 DÉMARRAGE DU TEST LOCAL (HUMAN-LIKE) SUR : {url}")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, # Mkhalyinha False lel test
                args=["--disable-blink-features=AutomationControlled"]
            ) 
            
            for i in range(max_orders):
                user = users[i]
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
                    viewport={"width": 1280, "height": 720}
                )
                
                context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined })
                """)
                
                page = context.new_page()
                log("-" * 50)
                log(f"▶️ [COMMANDE {i+1}/{max_orders}] Remplissage en cours...")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    
                    # SCROLLING HUMAIN (B'la39el)
                    for j in range(1, 6):
                        page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * ({j} / 5))")
                        time.sleep(random.uniform(0.5, 1.2)) # Ystena chwiya bin kol scroll
                    
                    # 1. NOM (Typing Humain)
                    name_input = page.locator("input:not([type='tel']):not([name*='phone' i]):not([id*='phone' i]):not([placeholder*='هاتف' i])[name*='name' i], input:not([type='tel'])[placeholder*='اسم' i], input:not([type='tel'])[placeholder*='nom' i]").first
                    if name_input.count() > 0:
                        name_input.scroll_into_view_if_needed()
                        name_input.click() # Y-kiliki f' l'khana qbel ma yekteb (kima l'insan)
                        time.sleep(random.uniform(0.3, 0.8)) # Y-khmem chwiya
                        name_input.press_sequentially(user["nom"], delay=random.randint(150, 250)) # Yekteb b'la39el w delay عشوائي
                        log(f"   👁️ [RADAR] Nom injecté : {user['nom']}")
                    
                    time.sleep(random.uniform(0.5, 1.5)) # Pause bin l'khana w lokhra

                    # 2. TÉLÉPHONE (Typing Humain)
                    phone_input = page.locator("input[type='tel'], input[placeholder*='هاتف' i], input[placeholder*='تليفون' i], input[name*='phone' i], input[id*='phone' i]").first
                    if phone_input.count() > 0:
                        phone_input.scroll_into_view_if_needed()
                        phone_input.evaluate("el => el.value = ''") 
                        phone_input.click()
                        time.sleep(random.uniform(0.3, 0.8))
                        phone_input.press_sequentially(user["telephone"], delay=random.randint(150, 250))
                        phone_input.blur()
                        log(f"   👁️ [RADAR] Tél injecté : {user['telephone']}")

                    time.sleep(random.uniform(0.5, 1.5))

                    # 3. UNIVERSEL (Typing Humain)
                    all_inputs = page.locator("input[type='text'], input:not([type]), textarea")
                    for j in range(all_inputs.count()):
                        try:
                            inp = all_inputs.nth(j)
                            if inp.is_visible() and not inp.input_value(): 
                                inp.scroll_into_view_if_needed()
                                inp.click()
                                time.sleep(random.uniform(0.2, 0.5))
                                inp.press_sequentially(user["adresse_generique"], delay=random.randint(100, 200))
                                time.sleep(random.uniform(0.3, 0.7))
                        except:
                            pass

                    all_selects = page.locator("select")
                    for j in range(all_selects.count()):
                        try:
                            sel = all_selects.nth(j)
                            if sel.is_visible():
                                time.sleep(random.uniform(0.5, 1.0))
                                sel.select_option(index=1) 
                        except:
                            pass

                    log("   ✅ [RADAR] Formulaire rempli avec succès.")
                    time.sleep(random.uniform(1.5, 3.0)) # Y-khmem qbel ma y-kiliki "Commander"

                    # 4. CLIC FINAL
                    submit_btn = page.locator("button:has-text('شراء'), button:has-text('طلب'), button:has-text('تأكيد'), button:has-text('Commander'), input[type='submit']").last
                    if submit_btn.count() == 0:
                        submit_btn = page.locator("button").last

                    if submit_btn.is_visible():
                        submit_btn.scroll_into_view_if_needed()
                        # Simulation d'un vrai clic de souris (plus naturel que javascript click)
                        submit_btn.hover()
                        time.sleep(random.uniform(0.2, 0.5))
                        submit_btn.click() 
                        log("   🖱️ Clic effectué !")
                        
                        time.sleep(8) 
                        
                        url_apres = page.url
                        page_text = page.content().lower()

                        if url_apres != url or "thank" in url_apres or "شكرا" in page_text or "merci" in page_text:
                            log(f"   🟢 [RÉSULTAT] : SUCCÈS ! Commande Validée !")
                        else:
                            log(f"   🔴 [RÉSULTAT] : ÉCHEC. L'URL n'a pas bougé.")
                    else:
                        log(f"   🔴 [ERREUR] Bouton invisible.")

                except Exception as e:
                    log(f"   🔴 [ERREUR TECHNIQUE] : {str(e)}")
                finally:
                    time.sleep(5)
                    context.close() 
            
            browser.close()

if __name__ == "__main__":
    URL_CIBLE = "https://libyaworld.youcan.store/products/salatlibia" 
    bot = StoreBot()
    bot.execute_stress_test(url=URL_CIBLE, max_orders=1)
