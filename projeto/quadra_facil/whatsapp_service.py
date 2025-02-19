from twilio.rest import Client
import os

# Pegando variáveis de ambiente
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

def enviar_mensagem_whatsapp(nome_reservante, telefone_reservante, horario):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    mensagem = f"Olá {nome_reservante}, sua reserva foi confirmada! 🏀\n\n"
    mensagem += f"📅 Data/Horário: {horario.data_hora}\n"
    mensagem += f"📍 Quadra: {horario.quadra.nome}\n\n"
    mensagem += "Aguardamos você! 😊"

    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{telefone_reservante}",
        body=mensagem
    )

    return message.sid  # Retorna o ID da mensagem
