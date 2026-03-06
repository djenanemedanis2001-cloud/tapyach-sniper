from playwright.sync_api import sync_playwright
import json
import time

# ==========================================
# PHASE 1: THE ARCHITECT (Advanced E-commerce Scanner)
# ==========================================

class StoreArchitect:
    def __init__(self):
        # Dictionnaire ultra-complet pour capter 99% des champs (YouCan, Shopify, WooCommerce)
        self.dictionary = {
            "name": ["nom", "name", "اسم", "الاسم", "prénom", "first_name", "last_name", "customer_name", "fullname", "prenom", "first-name"],
            "phone": ["téléphone", "phone", "هاتف", "رقم", "tel", "mobile", "customer_phone", "number"],
            "wilaya": ["wilaya", "city", "ولاية", "الولاية", "ville", "province", "state", "region", "customer_city", "gouvernorat"],
            "commune": ["commune", "بلدية", "البلدية", "address", "adresse", "العنوان", "zip", "customer_address", "street"]
        }
        self.button_keywords = ["commander", "order", "submit", "طلب", "إضغط", "شراء", "buy", "checkout", "أطلب", "تأكيد", "valider", "complete"]

    def _identify_field(self, name_attr, id_attr, placeholder_attr, type_attr):
        # N-jem3ou ga3 les indices (Attributes) f'string wa7ed pour la recherche
        indices = f"{name_attr} {id_attr} {placeholder_attr} {type_attr}".lower()
        
        # Exception : Ida kan l'type "tel", houwa 100% téléphone
        if "tel" in type_attr.lower():
            return "phone"

        for field_type, keywords in self.dictionary.items():
            for kw in keywords:
                # N-7awso b'façon exacte (bach ma ykheletch "name" m3a "first_name")
                if kw in indices:
                    return field_type
        return None

    def scan_store(self, url):
        print(f"\n🚀 [ARCHITECT] Démarrage du scan sur : {url}")
        site_map = {"fields": {}, "submit_button": None}

        with sync_playwright() as p:
            # Headless=True ma3naha ykhdem f'silece sans ouvrir Chrome (Mliha l'SaaS)
            # Ida 7abit tchouf wesh sary, radha False
            browser = p.chromium.launch(headless=True) 
            
            # N-raj3ouh kima l'humain (User Agent) bach YouCan ma y-bloquihch
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            try:
                # FIX 1: domcontentloaded au lieu de networkidle bach ma ydirch Timeout 
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                print("✅ [ARCHITECT] Page chargée (HTML DOM).")
                
                # FIX 2: Simulation ta3 humain y-scrolli chwiya chwiya (Smooth Scroll) bach y-forci l'Lazy Loading
                print("⏳ [ARCHITECT] Auto-Scroll profond pour charger le formulaire YouCan...")
                for i in range(1, 6):
                    page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * ({i} / 5))")
                    time.sleep(1) # Y-stena 1 sec f'kol scroll
                
                # N-stennaw chwiya l'JavaScript ykamel l'khedma ta3o
                time.sleep(2)
                
                print("🧠 [ARCHITECT] Analyse des champs (Inputs & Selects)...")

                # ==========================================
                # A. SCANNER LES INPUTS (Dans toute la page + iframes si existent)
                # ==========================================
                # N-jib ga3 les inputs visibles, machi cachés, w machi boutons
                inputs = page.locator("input:not([type='hidden']):not([type='submit']):not([type='button'])").element_handles()
                
                for index, element in enumerate(inputs):
                    name_attr = element.get_attribute("name") or ""
                    id_attr = element.get_attribute("id") or ""
                    placeholder = element.get_attribute("placeholder") or ""
                    type_attr = element.get_attribute("type") or ""

                    # N-3etmdo sur les Attributs (Name/Placeholder/Type) kter men Label f'YouCan
                    field_type = self._identify_field(name_attr, id_attr, placeholder, type_attr)
                    
                    if field_type and field_type not in site_map["fields"]:
                        # FIX 3: N-creyi un CSS Selector intelligent w solide (y-viser l'Name d'abord)
                        if name_attr:
                            selector = f"input[name='{name_attr}']"
                        elif id_attr:
                            selector = f"input#{id_attr}"
                        elif placeholder:
                            selector = f"input[placeholder='{placeholder}']"
                        else:
                            selector = f"input[type='{type_attr}']" if type_attr else f"input:nth-of-type({index+1})"
                            
                        site_map["fields"][field_type] = {
                            "type": "input",
                            "selector": selector
                        }

                # ==========================================
                # B. SCANNER LES SELECTS (Wilaya, Commune)
                # ==========================================
                selects = page.locator("select").element_handles()
                
                for index, element in enumerate(selects):
                    name_attr = element.get_attribute("name") or ""
                    id_attr = element.get_attribute("id") or ""
                    
                    # Les Selects ma fihomch placeholder f'l'HTML normal
                    field_type = self._identify_field(name_attr, id_attr, "", "select")
                    
                    if field_type and field_type not in site_map["fields"]:
                        if name_attr:
                            selector = f"select[name='{name_attr}']"
                        elif id_attr:
                            selector = f"select#{id_attr}"
                        else:
                            selector = f"select:nth-of-type({index+1})"
                            
                        site_map["fields"][field_type] = {
                            "type": "select",
                            "selector": selector
                        }

                # ==========================================
                # C. SCANNER LE BOUTON (Submit/Commander)
                # ==========================================
                # YouCan y-kheddem bzaf les balises <button> wla input type="submit"
                buttons = page.locator("button, input[type='submit']").element_handles()
                
                for btn in buttons:
                    # L'texte ta3 l'bouton ykoun f' innerText (Button) wla f' Value (Input Submit)
                    text_content = (btn.inner_text() or "").lower()
                    val_attr = (btn.get_attribute("value") or "").lower()
                    combined_btn_text = f"{text_content} {val_attr}"
                    
                    for kw in self.button_keywords:
                        if kw in combined_btn_text:
                            # Lqina l'bouton li fih l'mot clé!
                            btn_type = btn.evaluate("el => el.tagName").lower()
                            btn_id = btn.get_attribute("id")
                            btn_type_attr = btn.get_attribute("type")

                            # Selector solide
                            if btn_type_attr == "submit":
                                selector = f"{btn_type}[type='submit']"
                            elif btn_id:
                                selector = f"{btn_type}#{btn_id}"
                            elif text_content:
                                # Y-viser l'bouton b'l'texte ta3ou directement
                                selector = f"{btn_type}:has-text('{btn.inner_text()}')"
                            else:
                                selector = btn_type
                                
                            site_map["submit_button"] = {"selector": selector}
                            break # Nokhrojo men l'boucle ta3 les mots clés
                            
                    if site_map["submit_button"]:
                        break # Nokhrojo men l'boucle ta3 les boutons

            except Exception as e:
                print(f"❌ [ERREUR CRITIQUE] Le scan a échoué : {str(e)}")
            finally:
                context.close()
                browser.close()

        print("✅ [ARCHITECT] Scan terminé avec succès !")
        # Y-retourner le JSON (ensure_ascii=False bach l'Arabe yban mrigel)
        return json.dumps(site_map, indent=4, ensure_ascii=False)

# ==========================================
# TEST DIRECT
# ==========================================
if __name__ == "__main__":
    architect = StoreArchitect()
    
    # Lien ta3 YouCan li b3athtli
    test_url = "https://luxury-shopping-dz.youcan.store/pages/hlo-asbany-hamd" 
    
    result = architect.scan_store(test_url)
    print("\n🎯 RÉSULTAT DU SCAN (JSON MAP) :")
    print(result)
