import os
import sys
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
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
        for i in range(count):
            users.append({
                "nom": f"Test Edu {random.randint(100, 999)}",
                "telephone": f"055{random.randint(1000000, 9999999)}",
                "adresse_generique": f"Cite Test {random.randint(1, 100)}, Alger"
            })
        return users

    def execute_stress_test(self, url, max_orders=5):
        users = self.get_user_data(max_orders)
        if not users: return

        log(f"\n🚀 DÉMARRAGE DU BOT (STEALTH CLOUD) SUR : {url}")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, 
                args=[
                    "--no-sandbox", 
                    "--disable-setuid-sandbox", 
                    "--disable-blink-features=AutomationControlled", # ⚠️ LE FIX ANTI-BOT EST ICI ⚠️
                    "--disable-dev-shm-usage"
                ]
            ) 
            
            for i in range(max_orders):
                user = users[i]
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1920, "height": 1080}
                )
                
                # ⚠️ LE SECRET DU CLOUD (INJECTION JS BACH Y-T5EBA L'BOT) ⚠️
                context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """)
                
                page = context.new_page()
                
                log("-" * 50)
                log(f"▶️ [COMMANDE {i+1}/{max_orders}] Remplissage en cours...")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    
                    for _ in range(3):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(1)

                    # 1. NOM
                    name_input = page.locator("input[name*='name' i], input[placeholder*='اسم' i], input[placeholder*='nom' i]").first
                    if name_input.count() > 0:
                        name_input.scroll_into_view_if_needed()
                        name_input.fill(user["nom"])
                    
                    # 2. TÉLÉPHONE
                    phone_input = page.locator("input[type='tel'], input[name*='phone' i], input[placeholder*='هاتف' i], input[placeholder*='téléphone' i]").first
                    if phone_input.count() > 0:
                        phone_input.scroll_into_view_if_needed()
                        phone_input.evaluate("el => el.value = ''") 
                        phone_input.click()
                        phone_input.press_sequentially(user["telephone"], delay=100)
                        phone_input.blur()
                        log(f"   👁️ [RADAR] Tél injecté: {user['telephone']}")

                    # 3. UNIVERSEL (REMPLIR TOUT LE RESTE)
                    all_inputs = page.locator("input[type='text'], input:not([type]), textarea")
                    for j in range(all_inputs.count()):
                        try:
                            inp = all_inputs.nth(j)
                            if inp.is_visible() and not inp.input_value():
                                inp.scroll_into_view_if_needed()
                                inp.fill(user["adresse_generique"])
                        except:
                            pass

                    all_selects = page.locator("select")
                    for j in range(all_selects.count()):
                        try:
                            sel = all_selects.nth(j)
                            if sel.is_visible():
                                sel.select_option(index=1) 
                        except:
                            pass

                    log("   ✅ [RADAR] Formulaire rempli (Mode Stealth).")
                    time.sleep(2) 

                    # 4. CLIC FINAL
                    submit_btn = page.locator("button:has-text('شراء'), button:has-text('طلب'), button:has-text('تأكيد'), button:has-text('Commander'), input[type='submit']").last
                    if submit_btn.count() == 0:
                        submit_btn = page.locator("button").last

                    if submit_btn.is_visible():
                        submit_btn.scroll_into_view_if_needed()
                        
                        # Clic JavaScript bach may-tbloquach
                        submit_btn.evaluate("el => el.click()")
                        log("   🖱️ Frappe du bouton Commander...")
                        
                        time.sleep(8) 
                        
                        url_apres = page.url
                        page_text = page.content().lower()

                        log(f"   🔎 [DEBUG] URL finale atteinte: {url_apres}")

                        # VÉRIFICATION STRICTE (Plus de faux positifs)
                        if "thank" in url_apres or "شكرا" in page_text or "merci" in page_text or "success" in page_text or "receipt" in url_apres:
                            log(f"   🟢 [RÉSULTAT {i+1}] : COMMANDE VALIDÉE ET ENVOYÉE 100% !")
                        else:
                            log(f"   🔴 [RÉSULTAT {i+1}] : ÉCHEC. Bloqué par l'anti-bot du site (Cloudflare).")
                    else:
                        log(f"   🔴 [ERREUR] Bouton invisible.")

                except Exception as e:
                    log(f"   🔴 [ERREUR TECHNIQUE {i+1}] : {str(e)}")
                finally:
                    context.close() 
                
                if i < max_orders - 1:
                    time.sleep(random.randint(4, 7))
            
            browser.close()
            log("\n🏁 MISSION TERMINÉE.")
