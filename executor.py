from playwright.sync_api import sync_playwright
import csv
import json
import time
import random

# ==========================================
# PHASE 2 : THE EXECUTOR (Test UI Automatisé)
# ==========================================

class StoreExecutor:
    def __init__(self, site_map_json, csv_file="data.csv"):
        # Y-chargi l'Khariṭa (Map) li jabha l'Architect
        self.site_map = json.loads(site_map_json)
        self.csv_file = csv_file

    def get_test_data(self, limit=3):
        """Ya9ra l'fichier data.csv w yjib les identités"""
        data = []
        try:
            with open(self.csv_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= limit: break
                    data.append(row)
            return data
        except FileNotFoundError:
            print("❌ Erreur: Le fichier 'data.csv' n'existe pas. Lancez le générateur d'abord.")
            return []

    def run_stress_test(self, url, test_count=3):
        print(f"\n🚀 [EXECUTOR] Démarrage des tests UI sur : {url}")
        test_data = self.get_test_data(limit=test_count)
        
        if not test_data:
            return

        with sync_playwright() as p:
            # headless=False bach tchouf l'Bot b'3inek kifech y-taper
            browser = p.chromium.launch(headless=False) 
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            for index, user in enumerate(test_data, 1):
                print(f"\n▶️ [TEST {index}/{test_count}] Remplissage pour: {user['nom']} ({user['telephone']})")
                page = context.new_page()
                
                try:
                    # 1. Aller sur le site
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    time.sleep(2) # Ystena chwiya bach l'JavaScript y-tchargé
                    
                    # Scroll kima f'Architect bach yban l'formulaire
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1)

                    # 2. Remplir les champs b'tariqa Human-Like
                    fields = self.site_map.get("fields", {})
                    
                    # Remplir le Nom
                    if "name" in fields:
                        selector = fields["name"]["selector"]
                        print(f"   ⌨️ Écriture du nom...")
                        # delay=100 ma3naha y-stena 100ms bin kol 7arf (Kima l'insan)
                        page.locator(selector).first.type(user["nom"], delay=100) 
                        page.locator(selector).first.blur() # Y-kheraj men l'champ bach y-déclenchi l'event

                    # Remplir le Téléphone
                    if "phone" in fields:
                        selector = fields["phone"]["selector"]
                        print(f"   📱 Écriture du téléphone...")
                        page.locator(selector).first.type(user["telephone"], delay=150)
                        page.locator(selector).first.blur()

                    # Remplir la Wilaya (Si c'est un input text f'YouCan wla select)
                    if "wilaya" in fields:
                        selector = fields["wilaya"]["selector"]
                        field_type = fields["wilaya"].get("type", "input")
                        
                        if field_type == "input":
                            print(f"   🌍 Écriture de la wilaya...")
                            page.locator(selector).first.type(user["wilaya"], delay=100)
                        elif field_type == "select":
                            print(f"   🌍 Sélection de la wilaya...")
                            page.locator(selector).first.select_option(label=user["wilaya"])

                    # 3. Cliquer sur le Bouton Commander
                    submit_info = self.site_map.get("submit_button")
                    if submit_info and "selector" in submit_info:
                        btn_selector = submit_info["selector"]
                        print(f"   🖱️ Clic sur le bouton de confirmation...")
                        # page.locator(btn_selector).first.click() # (Dé-commenti hadi f'le vrai test)
                        
                        # Juste pour le test visuel (y-highlighti l'bouton)
                        page.locator(btn_selector).first.evaluate("node => node.style.border = '3px solid red'")
                        print("   ✅ Simulation terminée avec succès (Clic désactivé pour la sécurité du test).")
                    
                    # Pause bin kol utilisateur w lakher
                    time.sleep(3)

                except Exception as e:
                    print(f"   ❌ Erreur pendant le test {index}: {str(e)}")
                finally:
                    page.close() # Y-ghlaq l'onglet
            
            browser.close()
            print("\n🎉 [EXECUTOR] Tous les tests sont terminés !")

# ==========================================
# TEST DIRECT
# ==========================================
if __name__ == "__main__":
    # Hada l'JSON li khrejlek nta f'l'étape ta3 l'Architect (La carte exacte)
    json_map_youcan = """
    {
        "fields": {
            "name": {
                "type": "input",
                "selector": "input[name='first_name']"
            },
            "phone": {
                "type": "input",
                "selector": "input[placeholder='رقم الهاتف 📞']"
            },
            "wilaya": {
                "type": "input",
                "selector": "input[name='extra_fields[custom_field_TzZLctj3l8OBqE87]']"
            }
        },
        "submit_button": {
            "selector": "button:has-text('شراء الآن')"
        }
    }
    """
    
    url_a_tester = "https://luxury-shopping-dz.youcan.store/pages/hlo-asbany-hamd"
    
    executor = StoreExecutor(site_map_json=json_map_youcan, csv_file="data.csv")
    
    # Y-sayi y-rempli 2 commandes bark pour le test
    executor.run_stress_test(url=url_a_tester, test_count=2)
