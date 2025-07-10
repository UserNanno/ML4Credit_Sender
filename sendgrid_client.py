from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, Personalization, CustomArg
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_email(to_emails, subject, html, delivery_code, usuario):
    message = Mail(
        from_email='notificaciones@ml4credit.com',
        to_emails=to_emails,
        subject=subject,
        html_content=html,
    )

    personalization = Personalization()
    for email in to_emails:
        personalization.add_to(To(email))

    personalization.add_custom_arg(CustomArg("delivery_code", delivery_code))
    personalization.add_custom_arg(CustomArg("usuario", usuario))

    message.add_personalization(personalization)

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        print("Email enviado")
        print("Status code:", response.status_code)
        print("Headers:", response.headers)
        print("Body:", response.body)

        if response.status_code == 202:
            print("SendGrid aceptó el correo correctamente.")
        else:
            print("⚠SendGrid respondió con código inesperado.")

    except Exception as e:
        print("Error al enviar correo con SendGrid:", str(e))
