from playwright.sync_api import sync_playwright
import time
import random

class StoreBot:
    def __init__(self, csv_file="data.csv"):
        pass # Ma n-s7a9ouch l'CSV f' l'Cloud, n-génériw la data direct

    def get_user_data(self, count):
        # Génération ta3 Data éducative f' l'RAM (Parfait pour le Cloud)
        users = []
        wilayas = ["Alger", "Oran", "Constantine", "Annaba", "Setif"]
        for i in range(count):
            users.append({
                "nom": f"Test Edu {random.randint(100, 999)}",
                "telephone": f"055{random.randint(1000000, 9999999)}",
                "wilaya": random.choice(wilayas),
                "adresse": f"Cite Test {random.randint(1, 100)}, {random.choice(wilayas)}"
            })
        return users

    def execute_stress_test(self, url, max_orders=5):
        users = self.get_user_data(max_orders)
        if not users: return

        print(f"\n🚀 DÉMARRAGE DU BOT SUR : {url}")

        with sync_playwright() as p:
            # FIX RENDER : Lazem headless=True w les args ta3 Linux bach ma y-plantach
            browser = p.chromium.launch(
                headless=True, 
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            ) 
            
            for i in range(max_orders):
                user = users[i]
                # Stealth Mode bach y-ban kima PC vrai f' l'Cloud
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
                    viewport={"width": 1920, "height": 1080}
                )
                page = context.new_page()
                
                print("-" * 50)
                print(f"▶️ [COMMANDE {i+1}/{max_orders}] Remplissage pour : {user['nom']}")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    for _ in range(3):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(1)

                    # A. Le Nom
                    name_input = page.locator("input[name='first_name'], input[name='name'], input[placeholder*='اسم' i], input[placeholder*='nom' i]").first
                    if name_input.count() > 0:
                        name_input.scroll_into_view_if_needed()
                        name_input.fill(user["nom"])
                    
                    # B. Le Téléphone
                    phone_input = page.locator("input[name='phone'], input[type='tel'], input[placeholder*='هاتف' i], input[placeholder*='téléphone' i]").first
                    if phone_input.count() > 0:
                        phone_input.scroll_into_view_if_needed()
                        phone_input.evaluate("el => el.value = ''") 
                        phone_input.click()
                        phone_input.press_sequentially(user["telephone"], delay=50)
                        phone_input.blur()
                        print(f"   📱 Téléphone injecté : {user['telephone']}")

                    # C. La Wilaya
                    wilaya_input = page.locator("input[placeholder*='ولاية' i], select[name*='city'], input[name*='extra_fields']").first
                    if wilaya_input.count() > 0:
                        wilaya_input.scroll_into_view_if_needed()
                        if wilaya_input.evaluate("el => el.tagName").lower() == "select":
                            wilaya_input.select_option(label=user["wilaya"])
                        else:
                            wilaya_input.fill(user["wilaya"])

                    # D. La Commune / Adresse
                    commune_input = page.locator("input[placeholder*='بلدية' i], input[name='city'], input[placeholder*='عنوان' i]").first
                    if commune_input.count() > 0:
                        commune_input.scroll_into_view_if_needed()
                        commune_input.evaluate("el => el.value = ''")
                        commune_input.click()
                        commune_input.press_sequentially(user["adresse"], delay=30)

                    time.sleep(1) 

                    # LE CLIC ET LA VÉRIFICATION
                    print("   🖱️ Clic sur 'Commander'...")
                    submit_btn = page.locator("button:has-text('شراء'), button:has-text('طلب'), button:has-text('تأكيد'), button:has-text('Commander'), input[type='submit']").last
                    if submit_btn.count() == 0:
                        submit_btn = page.locator("button").last

                    submit_btn.scroll_into_view_if_needed()
                    url_avant = page.url
                    submit_btn.click(force=True)
                    
                    print("   ⏳ Validation en cours...")
                    time.sleep(7) 
                    
                    url_apres = page.url
                    page_text = page.content().lower()

                    if url_apres != url_avant or "thank" in url_apres or "شكرا" in page_text or "merci" in page_text:
                        print(f"   🟢 [RÉSULTAT {i+1}] : LA COMMANDE EST PASSÉE AVEC SUCCÈS !")
                    else:
                        print(f"   🔴 [RÉSULTAT {i+1}] : ÉCHEC DE LA COMMANDE.")

                except Exception as e:
                    print(f"   🔴 [ERREUR TECHNIQUE {i+1}] : {str(e)}")
                finally:
                    context.close() 
                
                # Pause pour pas bloquer le serveur
                if i < max_orders - 1:
                    time.sleep(random.randint(5, 10))
            
            browser.close()
            print("\n🏁 TOUTES LES COMMANDES SONT TERMINÉES.")
