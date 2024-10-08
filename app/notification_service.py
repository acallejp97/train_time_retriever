from apprise import Apprise
from utils import get_datetime
import os


class NotificationService:

    def __init__(self):
        self.service = Apprise()
        self.notification_bot = os.environ.get("NOTIFICATION_URL")

    def send_message(self, messages, origin_name, destination_name):
        if len(messages) == 1:
            messages.append("No hay trenes disponibles")
        self.service.add(self.notification_bot)
        body = f"Origen: {origin_name} - Destino: {destination_name}\n"
        for message in messages:
            body += f"{message}\n"
        self.service.notify(title=f"Train Schedule {str(get_datetime().strftime('%Y-%m-%d %H:%M'))}", body=body)
        print(f"Mensaje enviado con {len(messages) - 1} horarios")
