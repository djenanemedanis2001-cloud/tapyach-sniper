# sniper_engine.py
from architect import StoreArchitect
from generator_pro import DZDataGenerator
from main_bot import StoreBot
import json

class SniperMaster:
    def __init__(self):
        self.architect = StoreArchitect()
        self.generator = DZDataGenerator()
        self.bot = StoreBot()

    def run_full_mission(self, url, order_count=5):
        print(f"🎯 MISSION STARTED ON: {url}")
        
        # 1. SCAN (Architect)
        print("🔍 Step 1: Scanning Store Layout...")
        site_map = self.architect.scan_store(url)
        
        # 2. DATA (Generator)
        print(f"📊 Step 2: Generating {order_count} DZ Identities...")
        self.generator.generate_identities(count=order_count)
        
        # 3. EXECUTE (Bot)
        print("🤖 Step 3: Launching Tactical Orders...")
        self.bot.execute_stress_test(url, max_orders=order_count)
        
        return {"status": "Mission Complete"}