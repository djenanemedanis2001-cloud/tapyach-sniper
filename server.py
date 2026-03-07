from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from main_bot import StoreBot

app = FastAPI(title="Sniper SaaS API")

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

@app.post("/launch")
def launch_sniper(request: MissionRequest):
    print(f"⚙️ [MISSION] Démarrage du Sniper sur {request.url} pour {request.orders} commandes...")
    
    # ⚠️ L'ASTUCE ICI: N-khaliw l'API t-stena l'Bot 7ata y-kamel ga3 l'Boucle qbel ma n-rodou l'Vercel.
    try:
        bot = StoreBot(csv_file="data.csv")
        bot.execute_stress_test(url=request.url, max_orders=request.orders)
        print("✅ [MISSION] Terminé avec succès.")
        
        return {
            "status": "success",
            "message": f"🚀 Missiles lancés: {request.orders} commandes sur {request.url}"
        }
    except Exception as e:
        print(f"❌ [MISSION] Erreur Critique: {e}")
        return {
            "status": "error",
            "message": f"Erreur: {str(e)}"
        }

if __name__ == "__main__":
    print("🌐 Serveur SNIPER API actif sur le port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
