import os
from datetime import datetime


def get_datetime():
    return datetime.now()

def get_time():
    return get_datetime().strftime("%H:%M")

def as_time(time):
    return datetime.strptime(time, "%H:%M")

def get_bot_token():
    token = os.environ.get("NOTIFICATION_URL", "None").split("/")
    if token[0] != "None":
        return token[-2]
    raise ValueError("Token not found")
