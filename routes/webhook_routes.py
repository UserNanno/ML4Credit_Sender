from fastapi import APIRouter, Request
from database import SessionLocal
from sqlalchemy import text
from datetime import datetime
import json

router = APIRouter()

@router.post("/sendgrid/webhook")
async def recibir_webhook(request: Request):
    data = await request.json()
    print("📬 Webhook recibido:", data)

    # Guardar en archivo para debug
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f"evento_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    db = SessionLocal()
    try:
        for evento in data:
            try:
                db.execute(text("""
                    INSERT INTO tracking_eventos (
                        email, evento, timestamp, delivery_code, ip, user_agent
                    ) VALUES (:email, :evento, :ts, :code, :ip, :ua)
                """), {
                    "email": evento.get("email"),
                    "evento": evento.get("event"),
                    "ts": evento.get("timestamp"),
                    "code": evento.get("delivery_code"),
                    "ip": evento.get("ip", ""),
                    "ua": evento.get("useragent", "")
                })
            except Exception as e:
                print("❌ Error al insertar evento:", e)
        db.commit()
    finally:
        db.close()

    return {"status": "ok"}
