from train_schedule import TrainSchedule
from constants import NUCLEOS
from constants import ESTACIONES
from notification_service import NotificationService
import os
import argparse


def main(origin, destination):
    city = os.environ.get("CITY", "BILBAO").upper()
    origin_station = origin.upper()
    destination_station = destination.upper()
    threshold = os.environ.get("TIME_THRESHOLD", 1)

    core = NUCLEOS[city]
    origin = ESTACIONES[core][origin_station]
    destination = ESTACIONES[core][destination_station]

    train_service = TrainSchedule(core, origin, destination, threshold)
    schedules = train_service.get_train_schedule()
    NotificationService().send_message(schedules, origin_station, destination_station)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("origin")
    parser.add_argument("destination")

    args = parser.parse_args()

    main(args.origin, args.destination)
