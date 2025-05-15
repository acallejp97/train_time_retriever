import requests
import json
from constants import POST_URL
from utils import as_time
from utils import get_datetime
from utils import get_time


class TrainSchedule:
    def __init__(self, core, origin, destination, threshold):
        self.core = core
        self.date = get_datetime().strftime("%Y%m%d")
        self.departure = get_datetime().hour
        self.arrival = self.departure + int(threshold)
        self.origin = origin
        self.destination = destination

    def get_train_schedule(self):
        request_string = self.create_request()
        r = requests.post(POST_URL, data=request_string)
        try:
            response = r.json()
            print(response)
            response_as_json = response["horario"]
            schedules = []
            for train in response_as_json:
                if train["linea"] != "C4" and as_time(train["horaSalida"]) >= as_time(get_time()):
                    schedules.append(
                        f"{train['linea']} - {train['horaSalida']} - {train['horaLlegada']} - {train['duracion']}"
                    )
        except KeyError:
            schedules = ["Ha habido un error con la petición"]
        finally:
            return schedules

    def create_request(self):
        request_body = {
            "accesibilidadTrenes": False,
            "destino": self.destination,
            "fchaViaje": self.date,
            "horaViajeLlegada": self.arrival,
            "horaViajeOrigen": self.departure,
            "nucleo": self.core,
            "origen": self.origin,
            "servicioHorarios": "VTI",
            "tiempoReal": False,
            "validaReglaNegocio": True,
            "cdgoTerminal": "000000",
            "cdgoAplicacion": "CER",
        }
        return json.dumps(request_body)
