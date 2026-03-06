import os
import sys
# Forcer la sauvegarde de Chrome f' l'projet
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
# Forcer l'affichage direct f' les logs ta3 Render
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

        log(f"\n🚀 DÉMARRAGE DU BOT UNIVERSEL SUR : {url}")

        with sync_playwright() as p:
            # Mode Ultra-Khfif bach l'serveur gratuit ma y-plantach
            browser = p.chromium.launch(
                headless=True, 
                args=[
                    "--no-sandbox", 
                    "--disable-setuid-sandbox", 
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process",
                    "--no-zygote"
                ]
            ) 
            
            for i in range(max_orders):
                user = users[i]
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
                    viewport={"width": 1280, "height": 720}
                )
                page = context.new_page()
                
                # N-bloquiw tsawer w les fonts bach n-khefou l'chargement f' l'Cloud
                page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font"] else route.continue_())
                
                log("-" * 50)
                log(f"▶️ [COMMANDE {i+1}/{max_orders}] Remplissage en cours...")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    # Scroll auto bach y-beyen ga3 l'formulaire
                    for _ in range(3):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(1)

                    # 1. REMPLISSAGE DU NOM
                    name_input = page.locator("input[name*='name' i], input[placeholder*='اسم' i], input[placeholder*='nom' i]").first
                    if name_input.count() > 0:
                        name_input.scroll_into_view_if_needed()
                        name_input.fill(user["nom"])
                        log("   👁️ [RADAR] Nom injecté.")
                    
                    # 2. REMPLISSAGE DU TÉLÉPHONE
                    phone_input = page.locator("input[type='tel'], input[name*='phone' i], input[placeholder*='هاتف' i], input[placeholder*='téléphone' i]").first
                    if phone_input.count() > 0:
                        phone_input.scroll_into_view_if_needed()
                        phone_input.evaluate("el => el.value = ''") 
                        phone_input.click()
                        phone_input.press_sequentially(user["telephone"], delay=50)
                        phone_input.blur()
                        log(f"   👁️ [RADAR] Tél injecté: {user['telephone']}")

                    # 3. LE MODE UNIVERSEL (REMPLIR TOUT LE RESTE)
                    log("   👁️ [RADAR] Scan et remplissage des champs restants...")
                    
                    # N-jibou ga3 les inputs ta3 l'ktiba li f' l'page
                    all_inputs = page.locator("input[type='text'], input:not([type]), textarea")
                    
                    for j in range(all_inputs.count()):
                        try:
                            inp = all_inputs.nth(j)
                            # Ida kan l'input y-ban f' l'écran w mazal fargh (Value = vide)
                            if inp.is_visible():
                                val = inp.input_value()
                                if not val:
                                    inp.scroll_into_view_if_needed()
                                    inp.fill(user["adresse_generique"])
                        except Exception:
                            pass # N-foutouh ida fih mochkil

                    # N-dirou la meme chose l' ay menu déroulant (Select)
                    all_selects = page.locator("select")
                    for j in range(all_selects.count()):
                        try:
                            sel = all_selects.nth(j)
                            if sel.is_visible():
                                sel.select_option(index=1) # Y-kheyer l'option zawja
                        except Exception:
                            pass

                    log("   ✅ [RADAR] Tous les champs trouvés ont été remplis.")
                    time.sleep(1) 

                    # 4. LE CLIC FINAL
                    log("   🖱️ Frappe du bouton Commander...")
                    time.sleep(2) 

                    submit_btn = page.locator("button:has-text('شراء'), button:has-text('طلب'), button:has-text('تأكيد'), button:has-text('Commander'), input[type='submit']").last
                    if submit_btn.count() == 0:
                        submit_btn = page.locator("button").last

                    if submit_btn.is_visible():
                        submit_btn.scroll_into_view_if_needed()
                        url_avant = page.url
                        
                        submit_btn.click(force=True)
                        log("   ⏳ Attente confirmation Serveur (10s)...")
                        time.sleep(10) 
                        
                        url_apres = page.url
                        page_text = page.content().lower()

                        if url_apres != url_avant or "thank" in url_apres or "شكرا" in page_text or "merci" in page_text or "success" in page_text:
                            log(f"   🟢 [RÉSULTAT {i+1}] : COMMANDE VALIDÉE ET ENVOYÉE 100% !")
                        else:
                            log(f"   🔴 [RÉSULTAT {i+1}] : ÉCHEC. L'URL n'a pas changé.")
                    else:
                        log(f"   🔴 [ERREUR] Bouton non cliquable.")

                except Exception as e:
                    log(f"   🔴 [ERREUR TECHNIQUE {i+1}] : {str(e)}")
                finally:
                    context.close() 
                
                if i < max_orders - 1:
                    time.sleep(random.randint(4, 7))
            
            browser.close()
            log("\n🏁 MISSION TERMINÉE.")