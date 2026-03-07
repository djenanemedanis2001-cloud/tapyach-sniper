import os
import sys
# Forcer la sauvegarde de Chrome f' l'projet w l'affichage des logs
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

        log(f"\n🚀 DÉMARRAGE DU BOT (CLOUD MODE) SUR : {url}")

        with sync_playwright() as p:
            # FIX RENDER : Headless=True w les params ta3 Linux bach ma y-koulsh l'RAM
            browser = p.chromium.launch(
                headless=True, 
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process",
                    "--disable-blink-features=AutomationControlled"
                ]
            ) 
            
            for i in range(max_orders):
                user = users[i]
                # STEALTH MODE: Y-ban kima PC vrai
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
                    viewport={"width": 1280, "height": 720}
                )
                
                context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined })
                """)
                
                page = context.new_page()
                
                # Bloquer les images bach n-kheffou l'chargement
                page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font"] else route.continue_())

                log("-" * 50)
                log(f"▶️ [COMMANDE {i+1}/{max_orders}] Remplissage en cours...")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    
                    # SCROLLING
                    for j in range(1, 6):
                        page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * ({j} / 5))")
                        time.sleep(random.uniform(0.5, 1.2))
                    
                    # 1. NOM
                    name_input = page.locator("input:not([type='tel']):not([name*='phone' i]):not([id*='phone' i]):not([placeholder*='هاتف' i])[name*='name' i], input:not([type='tel'])[placeholder*='اسم' i], input:not([type='tel'])[placeholder*='nom' i]").first
                    if name_input.count() > 0:
                        name_input.scroll_into_view_if_needed()
                        name_input.click() 
                        time.sleep(random.uniform(0.3, 0.8)) 
                        name_input.press_sequentially(user["nom"], delay=random.randint(100, 200))
                        log(f"   👁️ [RADAR] Nom injecté : {user['nom']}")
                    
                    time.sleep(random.uniform(0.5, 1.5))

                    # 2. TÉLÉPHONE
                    phone_input = page.locator("input[type='tel'], input[placeholder*='هاتف' i], input[placeholder*='تليفون' i], input[name*='phone' i], input[id*='phone' i]").first
                    if phone_input.count() > 0:
                        phone_input.scroll_into_view_if_needed()
                        phone_input.evaluate("el => el.value = ''") 
                        phone_input.click()
                        time.sleep(random.uniform(0.3, 0.8))
                        phone_input.press_sequentially(user["telephone"], delay=random.randint(100, 200))
                        phone_input.blur()
                        log(f"   👁️ [RADAR] Tél injecté : {user['telephone']}")

                    time.sleep(random.uniform(0.5, 1.5))

                    # 3. UNIVERSEL (REMPLIR LE RESTE)
                    all_inputs = page.locator("input[type='text'], input:not([type]), textarea")
                    for j in range(all_inputs.count()):
                        try:
                            inp = all_inputs.nth(j)
                            if inp.is_visible() and not inp.input_value(): 
                                inp.scroll_into_view_if_needed()
                                inp.click()
                                time.sleep(random.uniform(0.2, 0.5))
                                inp.press_sequentially(user["adresse_generique"], delay=random.randint(50, 150))
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

                    log("   ✅ [RADAR] Formulaire rempli avec succès.")
                    time.sleep(random.uniform(1.5, 3.0))

                    # 4. CLIC FINAL
                    submit_btn = page.locator("button:has-text('شراء'), button:has-text('طلب'), button:has-text('تأكيد'), button:has-text('Commander'), input[type='submit']").last
                    if submit_btn.count() == 0:
                        submit_btn = page.locator("button").last

                    if submit_btn.is_visible():
                        submit_btn.scroll_into_view_if_needed()
                        # Clic JavaScript (Plus fiable f' l'Cloud)
                        submit_btn.evaluate("el => el.click()")
                        log("   🖱️ Clic effectué !")
                        
                        log("   ⏳ Attente co
