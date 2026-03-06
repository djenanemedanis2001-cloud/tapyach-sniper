from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from main_bot import StoreBot

app = FastAPI(title="Sniper SaaS API")

# N-khalou l'Interface tahder m3a l'API bla mochkil ta3 Sécurité
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MissionRequest(BaseModel):
    url: str
    orders: int = 5

def execute_mission(target_url: str, orders_count: int):
    print(f"⚙️ [MISSION] Démarrage du Sniper sur {target_url}...")
    try:
        bot = StoreBot(csv_file="data.csv")
        bot.execute_stress_test(url=target_url, max_orders=orders_count)
        print("✅ [MISSION] Terminé avec succès.")
    except Exception as e:
        print(f"❌ [MISSION] Erreur Critique: {e}")

@app.post("/launch")
def launch_sniper(request: MissionRequest, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(execute_mission, request.url, request.orders)
    return {
        "status": "success",
        "message": f"🚀 Missiles lancés sur {request.url}"
    }

if __name__ == "__main__":
    print("🌐 Serveur SNIPER API actif sur le port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
