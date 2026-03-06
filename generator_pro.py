import csv
import random
import time

# ==========================================
# DATA ENGINE : GÉNÉRATEUR AVANCÉ (PRO) 🇩🇿
# ==========================================

class DZDataGenerator:
    def __init__(self):
        # 1. Prénoms et Noms Algériens (Plus de variété pour éviter les doublons)
        self.first_names = [
            "Mohamed", "Amine", "Yacine", "Karim", "Sofiane", "Walid", "Hichem", "Omar", "Bilel", "Youcef", 
            "Abderrahmane", "Ayoub", "Hamza", "Fares", "Nassim", "Tarek", "Riyad", "Islam", "Ishak", "Zaki",
            "Fatima", "Amina", "Sarah", "Meriem", "Khadija", "Lina", "Ines", "Manel", "Kenza", "Rania"
        ]
        self.last_names = [
            "Saidi", "Benali", "Toumi", "Dahmani", "Zergui", "Kouri", "Brahimi", "Mansouri", "Mebarki", 
            "Bouzid", "Latreche", "Haddad", "Belkacem", "Meziani", "Slimani", "Hamidi", "Cherif", "Ait"
        ]

        # 2. Cartographie Cohérente (Wilaya -> Communes exactes)
        self.geo_data = {
            "Alger": ["Bab Ezzouar", "Hydra", "Rouiba", "Zeralda", "El Harrach", "Kouba"],
            "Oran": ["Es Senia", "Ain Turk", "Arzew", "Bir El Djir", "Gdyel"],
            "Blida": ["Boufarik", "Ouled Yaich", "Beni Mered", "Meftah", "El Affroun"],
            "Setif": ["El Eulma", "Ain Oulmene", "Bougaa", "Ain Arnat"],
            "Constantine": ["Khroub", "Zighoud Youcef", "Hamma Bouziane", "Ain Smara"],
            "Annaba": ["El Bouni", "Sidi Amar", "Berrahal", "El Hadjar"],
            "Tlemcen": ["Maghnia", "Remchi", "Mansourah", "Ghazaouet"]
        }

        # 3. Types de rues / cités pour le réalisme
        self.street_types = ["Rue", "Cité", "Avenue", "Boulevard", "Lotissement", "Quartier"]
        self.street_names = ["Emir Abdelkader", "1er Novembre", "5 Juillet", "Didouche Mourad", "Ben M'hidi", "de la Paix", "des Martyrs"]

    def generate_phone(self):
        """Génère un numéro de téléphone algérien valide (Regex-friendly)"""
        reseaux = [
            ("05", ["4", "5", "6"]), # Ooredoo
            ("06", ["5", "6", "7", "9"]), # Mobilis
            ("07", ["7", "8", "9"])  # Djezzy
        ]
        prefix_base, valid_seconds = random.choice(reseaux)
        prefix = f"{prefix_base}{random.choice(valid_seconds)}"
        rest = f"{random.randint(100000, 999999):06d}"
        return f"{prefix}{rest}"

    def generate_identities(self, count=100):
        print(f"⏳ [DATA ENGINE] Génération de {count} identités algériennes en cours...")
        start_time = time.time()
        
        identities = []
        wilayas_list = list(self.geo_data.keys())

        for _ in range(count):
            # Génération Nom complet
            full_name = f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
            
            # Génération Téléphone valide
            phone = self.generate_phone()
            
            # Génération Géographique cohérente
            wilaya = random.choice(wilayas_list)
            commune = random.choice(self.geo_data[wilaya])
            
            # Adresse réaliste
            street_type = random.choice(self.street_types)
            street_name = random.choice(self.street_names)
            batiment = random.randint(1, 150)
            adresse = f"{street_type} {street_name} N°{batiment}, {commune}"
            
            # Ajouter à la liste (Mémoire)
            identities.append([full_name, phone, adresse, commune, wilaya])

        # Batch Write (Écriture rapide en une seule fois)
        with open('data.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["nom", "telephone", "adresse", "commune", "wilaya"])
            writer.writerows(identities)

        execution_time = round(time.time() - start_time, 3)
        print(f"✅ [DATA ENGINE] Succès ! {count} identités sauvegardées dans 'data.csv' en {execution_time} secondes.")

# ==========================================
# TEST DIRECT
# ==========================================
if __name__ == "__main__":
    engine = DZDataGenerator()
    # Tqder tbedel l'nombre hna, sayi ddir 500 w chouf ch7al rapide!
    engine.generate_identities(count=500)
