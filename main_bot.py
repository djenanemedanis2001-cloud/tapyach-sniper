from playwright.sync_api import sync_playwright
import csv
import time
import random

class StoreBot:
    def __init__(self, csv_file="data.csv"):
        self.csv_file = csv_file

    def get_user_data(self):
        try:
            with open(self.csv_file, mode='r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except:
            print("❌ Fichier data.csv introuvable !")
            return []

    def execute_stress_test(self, url, max_orders=5):
        users = self.get_user_data()
        if not users: return

        print(f"\n🚀 DÉMARRAGE DU BOT SUR : {url}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False) 
            
            for i in range(max_orders):
                user = users[i]
                context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0")
                page = context.new_page()
                
                print("-" * 50)
                print(f"▶️ [COMMANDE {i+1}/{max_orders}] Remplissage pour : {user['nom']}")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    for _ in range(3):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(1)

                    # ==========================================
                    # A. Le Nom
                    # ==========================================
                    name_input = page.locator("input[name='first_name'], input[name='name'], input[placeholder*='اسم' i], input[placeholder*='nom' i]").first
                    if name_input.count() > 0:
                        name_input.scroll_into_view_if_needed()
                        name_input.fill(user["nom"])
                    
                    # ==========================================
                    # B. Le Téléphone (LE FIX INTELLIGENT HNA 🧠)
                    # ==========================================
                    phone_input = page.locator("input[name='phone'], input[type='tel'], input[placeholder*='هاتف' i], input[placeholder*='téléphone' i]").first
                    if phone_input.count() > 0:
                        phone_input.scroll_into_view_if_needed()
                        
                        # 1. N-ssagmo l'numéro ida kan fih 9 ar9am brk (Fix ta3 l'CSV)
                        phone_number = user["telephone"]
                        if len(phone_number) == 9:
                            phone_number += str(random.randint(0, 9)) # Nzidou ra9m bach yweli 10 exact
                        
                        # 2. N-naqiw l'khana b'JavaScript (Plus fiable)
                        phone_input.evaluate("el => el.value = ''") 
                        
                        # 3. N-tapiw b'la3qel w n-dirou Blur (bach YouCan y-dir la validation vert)
                        phone_input.click()
                        phone_input.press_sequentially(phone_number, delay=50)
                        phone_input.blur() # HADI HIYA LI T-CONFIRMI L'NUMÉRO F' YOUCAN
                        
                        print(f"   📱 Téléphone injecté : {phone_number}")

                    # ==========================================
                    # C. La Wilaya
                    # ==========================================
                    wilaya_input = page.locator("input[placeholder*='ولاية' i], select[name*='city'], input[name*='extra_fields']").first
                    if wilaya_input.count() > 0:
                        wilaya_input.scroll_into_view_if_needed()
                        if wilaya_input.evaluate("el => el.tagName").lower() == "select":
                            wilaya_input.select_option(label=user["wilaya"])
                        else:
                            wilaya_input.fill(user["wilaya"])

                    # ==========================================
                    # D. La Commune / Adresse
                    # ==========================================
                    commune_input = page.locator("input[placeholder*='بلدية' i], input[name='city'], input[placeholder*='عنوان' i]").first
                    if commune_input.count() > 0:
                        commune_input.scroll_into_view_if_needed()
                        commune_input.evaluate("el => el.value = ''")
                        commune_input.click()
                        commune_input.press_sequentially(user["adresse"], delay=30)

                    time.sleep(1) 

                    # ==========================================
                    # LE CLIC ET LA VÉRIFICATION 
                    # ==========================================
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
                        print(f"   🔴 [RÉSULTAT {i+1}] : ÉCHEC DE LA COMMANDE (Vérifie si y a un captcha).")

                except Exception as e:
                    print(f"   🔴 [ERREUR TECHNIQUE {i+1}] : {str(e)}")
                finally:
                    context.close() 
                
                # Pause pour pas bloquer le serveur
                if i < max_orders - 1:
                    pause_time = random.randint(10, 15)
                    print(f"   💤 Pause de {pause_time} sec...")
                    time.sleep(pause_time)
            
            browser.close()
            print("\n🏁 TOUTES LES COMMANDES SONT TERMINÉES.")

if __name__ == "__main__":
    URL_A_TESTER = "https://luxury-shopping-dz.youcan.store/pages/hlo-asbany-hamd" 
    
    bot = StoreBot()
    bot.execute_stress_test(url=URL_A_TESTER, max_orders=5)
