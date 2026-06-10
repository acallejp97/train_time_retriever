from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

from train_schedule import TrainSchedule


class TestTrainSchedule:
    @patch("train_schedule.get_datetime")
    def test_init(self, mock_get_datetime):
        """Test TrainSchedule initialization"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 0)
        train_schedule = TrainSchedule(60, 13206, 13200, 2)

        assert train_schedule.core == 60
        assert train_schedule.origin == 13206
        assert train_schedule.destination == 13200
        assert train_schedule.date == "20251225"
        assert train_schedule.departure == 14
        assert train_schedule.arrival == 16

    @patch("train_schedule.get_datetime")
    def test_init_with_string_threshold(self, mock_get_datetime):
        """Test TrainSchedule initialization with string threshold"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 10, 0)
        train_schedule = TrainSchedule(60, 13206, 13200, "1")

        assert train_schedule.arrival == 11

    @patch("train_schedule.get_datetime")
    def test_create_request(self, mock_get_datetime):
        """Test create_request method"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 0)
        train_schedule = TrainSchedule(60, 13206, 13200, 2)
        request = train_schedule.create_request()

        assert "20251225" in request
        assert '"nucleo": 60' in request
        assert '"origen": 13206' in request
        assert '"destino": 13200' in request
        assert '"horaViajeOrigen": 14' in request
        assert '"horaViajeLlegada": 16' in request
        assert '"accesibilidadTrenes": false' in request
        assert '"tiempoReal": false' in request

    @patch("train_schedule.requests.post")
    @patch("train_schedule.get_datetime")
    @patch("train_schedule.get_time")
    def test_get_train_schedule_success(self, mock_get_time, mock_get_datetime, mock_post):
        """Test get_train_schedule with successful response"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 0)
        mock_get_time.return_value = "14:00"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "horario": [
                {"linea": "R1", "horaSalida": "14:30", "horaLlegada": "15:30", "duracion": "1h"},
                {"linea": "C4", "horaSalida": "15:00", "horaLlegada": "16:00", "duracion": "1h"},
                {"linea": "R2", "horaSalida": "13:30", "horaLlegada": "14:30", "duracion": "1h"},
            ]
        }
        mock_post.return_value = mock_response

        train_schedule = TrainSchedule(60, 13206, 13200, 2)
        schedules = train_schedule.get_train_schedule()

        # Should include R1 (departure after current time), exclude C4, exclude R2 (departure before current time)
        assert len(schedules) == 1
        assert "R1 - 14:30 - 15:30 - 1h" in schedules

    @patch("train_schedule.requests.post")
    @patch("train_schedule.get_datetime")
    @patch("train_schedule.get_time")
    def test_get_train_schedule_no_trains(self, mock_get_time, mock_get_datetime, mock_post):
        """Test get_train_schedule with no valid trains"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 0)
        mock_get_time.return_value = "14:00"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "horario": [{"linea": "C4", "horaSalida": "15:00", "horaLlegada": "16:00", "duracion": "1h"}]
        }
        mock_post.return_value = mock_response

        train_schedule = TrainSchedule(60, 13206, 13200, 2)
        schedules = train_schedule.get_train_schedule()

        assert len(schedules) == 0

    @patch("train_schedule.requests.post")
    @patch("train_schedule.get_datetime")
    def test_get_train_schedule_api_error(self, mock_get_datetime, mock_post):
        """Test get_train_schedule when API returns error (missing horario key)"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 0)

        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "No trains available"}
        mock_post.return_value = mock_response

        train_schedule = TrainSchedule(60, 13206, 13200, 2)
        schedules = train_schedule.get_train_schedule()

        assert len(schedules) == 1
        assert schedules[0] == "Ha habido un error con la petición"

    @patch("train_schedule.requests.post")
    @patch("train_schedule.get_datetime")
    def test_get_train_schedule_json_parsing_error(self, mock_get_datetime, mock_post):
        """Test get_train_schedule when response.json() raises an exception"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 0)

        mock_response = MagicMock()
        mock_response.json.side_effect = KeyError("horario")
        mock_post.return_value = mock_response

        train_schedule = TrainSchedule(60, 13206, 13200, 2)
        schedules = train_schedule.get_train_schedule()

        # KeyError should be caught
        assert len(schedules) == 1
        assert schedules[0] == "Ha habido un error con la petición"

    @patch("train_schedule.requests.post")
    @patch("train_schedule.get_datetime")
    @patch("train_schedule.get_time")
    def test_get_train_schedule_multiple_trains(self, mock_get_time, mock_get_datetime, mock_post):
        """Test get_train_schedule with multiple valid trains"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 0)
        mock_get_time.return_value = "14:00"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "horario": [
                {"linea": "R1", "horaSalida": "14:30", "horaLlegada": "15:30", "duracion": "1h"},
                {"linea": "R2", "horaSalida": "15:00", "horaLlegada": "16:00", "duracion": "1h"},
                {"linea": "R3", "horaSalida": "16:00", "horaLlegada": "17:00", "duracion": "1h"},
            ]
        }
        mock_post.return_value = mock_response

        train_schedule = TrainSchedule(60, 13206, 13200, 2)
        schedules = train_schedule.get_train_schedule()

        assert len(schedules) == 3
        assert "R1 - 14:30 - 15:30 - 1h" in schedules
        assert "R2 - 15:00 - 16:00 - 1h" in schedules
        assert "R3 - 16:00 - 17:00 - 1h" in schedules

    @patch("train_schedule.requests.post")
    @patch("train_schedule.get_datetime")
    @patch("train_schedule.get_time")
    def test_get_train_schedule_train_at_exact_current_time(self, mock_get_time, mock_get_datetime, mock_post):
        """Test get_train_schedule with train at exact current time"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 0)
        mock_get_time.return_value = "14:00"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "horario": [{"linea": "R1", "horaSalida": "14:00", "horaLlegada": "15:00", "duracion": "1h"}]
        }
        mock_post.return_value = mock_response

        train_schedule = TrainSchedule(60, 13206, 13200, 2)
        schedules = train_schedule.get_train_schedule()

        # Train at exact current time should be included (>=)
        assert len(schedules) == 1
        assert "R1 - 14:00 - 15:00 - 1h" in schedules
