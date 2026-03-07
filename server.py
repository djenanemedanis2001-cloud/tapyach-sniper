import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
from main_bot import StoreBot
import threading
import queue

app = FastAPI(title="Sniper Live API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log_queue = queue.Queue()

# Hadi t-remplaci l'print normal bach t-b3ath l'Data l'Vercel
def custom_log(message):
    print(message, flush=True)
    log_queue.put(message)

def run_bot_in_thread(target_url, orders_count):
    try:
        bot = StoreBot(csv_file="data.csv")
        import main_bot
        main_bot.log = custom_log # Injecter notre log personnalisé
        
        bot.execute_stress_test(url=target_url, max_orders=orders_count)
        log_queue.put("DONE_SUCCESS")
    except Exception as e:
        log_queue.put(f"ERROR_FATAL: {str(e)}")

async def stream_logs(target_url: str, orders_count: int):
    thread = threading.Thread(target=run_bot_in_thread, args=(target_url, orders_count))
    thread.start()

    while True:
        try:
            msg = log_queue.get(timeout=1.0)
            if msg == "DONE_SUCCESS":
                yield f"data: {{\"type\": \"success\", \"msg\": \"✅ Mission terminée avec succès !\"}}\n\n"
                break
            elif str(msg).startswith("ERROR_FATAL"):
                yield f"data: {{\"type\": \"error\", \"msg\": \"❌ Erreur: {str(msg)}\"}}\n\n"
                break
            else:
                yield f"data: {{\"type\": \"info\", \"msg\": \"{msg}\"}}\n\n"
        except queue.Empty:
            yield ": ping\n\n"
            await asyncio.sleep(1)

# L'ENDPOINT Jdid li kan khass f' Render!
@app.get("/stream")
async def stream_sniper(url: str, orders: int):
    return StreamingResponse(stream_logs(url, orders), media_type="text/event-stream")

# N-kheliw l'ancien /launch k' Backup (Secours)
@app.post("/launch")
def fallback_launch():
    return {"status": "success", "message": "Use /stream instead"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
