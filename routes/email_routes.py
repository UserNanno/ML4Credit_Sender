from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from sendgrid_client import send_email
from database import SessionLocal
from sqlalchemy import text
import uuid

router = APIRouter()

class EmailRequest(BaseModel):
    to: List[str]
    subject: str
    html: str
    usuario: str

@router.post("/enviar-email")
def enviar_email(data: EmailRequest):
    delivery_code = str(uuid.uuid4())

    try:
        send_email(data.to, data.subject, data.html, delivery_code, data.usuario)
    except Exception as e:
        print("Error al enviar:", e)
        return {"error": f"Error al enviar: {str(e)}"}

    # Guardar historial
    db = SessionLocal()
    try:
        db.execute(text("""
            INSERT INTO historial_campanias_email (
                delivery_code, asunto, contenido_html, cantidad_destinatarios,
                destinatarios, usuario
            ) VALUES (:d, :a, :c, :n, :l, :u)
        """), {
            "d": delivery_code,
            "a": data.subject,
            "c": data.html,
            "n": len(data.to),
            "l": ",".join(data.to),
            "u": data.usuario
        })
        db.commit()
    except Exception as e:
        print("Error al guardar historial:", e)
    finally:
        db.close()

    return {"status": "ok", "delivery_code": delivery_code}
