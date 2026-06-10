import os
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from main import main


class TestMainFunction(unittest.TestCase):
    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO", "TIME_THRESHOLD": "1"})
    def test_main_creates_train_schedule(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main creates a TrainSchedule instance"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = []
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("AMETZOLA", "ABANDO")

        # Verify TrainSchedule was instantiated with correct parameters
        # core=60 (BILBAO), origin=13206 (AMETZOLA), destination=13200 (ABANDO), threshold=1
        mock_train_schedule_class.assert_called_once_with(60, 13206, 13200, "1")

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO"})
    def test_main_default_threshold(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main uses default threshold when not set"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = []
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("AMETZOLA", "ABANDO")

        # Verify threshold parameter is 1 (default)
        call_args = mock_train_schedule_class.call_args[0]
        assert call_args[3] == 1

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO", "TIME_THRESHOLD": "2"})
    def test_main_custom_threshold(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main uses custom threshold when set"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = []
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("AMETZOLA", "ABANDO")

        # Verify threshold parameter is 2
        call_args = mock_train_schedule_class.call_args[0]
        assert call_args[3] == "2"

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO"})
    def test_main_calls_get_train_schedule(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main calls get_train_schedule"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = ["Train R1"]
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("AMETZOLA", "ABANDO")

        # Verify get_train_schedule was called
        mock_train_schedule_instance.get_train_schedule.assert_called_once()

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO"})
    def test_main_sends_notification(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main sends notification with schedules"""
        schedules = ["Train R1 - 10:30", "Train R2 - 11:00"]
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = schedules
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("AMETZOLA", "ABANDO")

        # Verify send_message was called with correct parameters
        mock_notification_instance.send_message.assert_called_once_with(schedules, "AMETZOLA", "ABANDO")

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO"})
    def test_main_uppercase_stations(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main converts stations to uppercase"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = []
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("ametzola", "abando")

        # Verify stations were converted to uppercase
        mock_notification_instance.send_message.assert_called_once_with([], "AMETZOLA", "ABANDO")

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "bilbao"})  # lowercase city
    def test_main_uppercase_city(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main converts city to uppercase"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = []
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("AMETZOLA", "ABANDO")

        # Verify that event though city was lowercase, it was used correctly
        # The core should be 60 (for BILBAO)
        call_args = mock_train_schedule_class.call_args[0]
        assert call_args[0] == 60

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO"})
    def test_main_empty_schedules(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main handles empty schedules"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = []
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("AMETZOLA", "ABANDO")

        # Should still call send_message even with empty schedules
        mock_notification_instance.send_message.assert_called_once_with([], "AMETZOLA", "ABANDO")

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO"})
    def test_main_gets_correct_station_codes(self, mock_train_schedule_class, mock_notification_service_class):
        """Test that main gets correct station codes"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = []
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("AMETZOLA", "ABANDO")

        # Verify the station codes are correct
        # BILBAO (60), AMETZOLA (13206), ABANDO (13200)
        call_args = mock_train_schedule_class.call_args[0]
        assert call_args[0] == 60  # core
        assert call_args[1] == 13206  # origin (AMETZOLA)
        assert call_args[2] == 13200  # destination (ABANDO)

    @patch("main.NotificationService")
    @patch("main.TrainSchedule")
    @patch.dict(os.environ, {"CITY": "BILBAO"})
    def test_main_preserves_original_station_names_for_notification(
        self, mock_train_schedule_class, mock_notification_service_class
    ):
        """Test that original station names are used for notification"""
        mock_train_schedule_instance = MagicMock()
        mock_train_schedule_instance.get_train_schedule.return_value = []
        mock_train_schedule_class.return_value = mock_train_schedule_instance

        mock_notification_instance = MagicMock()
        mock_notification_service_class.return_value = mock_notification_instance

        main("ametzola", "abando")

        # Notification should receive uppercase names
        call_args = mock_notification_instance.send_message.call_args[0]
        assert call_args[1] == "AMETZOLA"
        assert call_args[2] == "ABANDO"


if __name__ == "__main__":
    unittest.main()
