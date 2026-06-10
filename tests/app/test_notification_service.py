import os
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

from notification_service import NotificationService


class TestNotificationService:
    @patch("notification_service.Apprise")
    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken/chatid"})
    def test_init(self, mock_apprise):
        """Test NotificationService initialization"""
        service = NotificationService()

        assert service.notification_bot == "tg://bottoken/chatid"
        mock_apprise.assert_called_once()

    @patch("notification_service.Apprise")
    def test_init_default_notification_url(self, mock_apprise):
        """Test NotificationService initialization with default notification URL"""
        with patch.dict(os.environ, {}, clear=True):
            service = NotificationService()
            assert service.notification_bot == "None"

    @patch("notification_service.get_datetime")
    @patch("notification_service.Apprise")
    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken/chatid"})
    def test_send_message_single_message(self, mock_apprise_class, mock_get_datetime):
        """Test send_message with a single message"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 14, 30)
        mock_apprise_instance = MagicMock()
        mock_apprise_class.return_value = mock_apprise_instance

        service = NotificationService()
        service.send_message(["Train R1 available"], "AMETZOLA", "ABANDO")

        # Verify add was called with the notification URL
        mock_apprise_instance.add.assert_called_once_with("tg://bottoken/chatid")

        # Verify notify was called
        mock_apprise_instance.notify.assert_called_once()
        call_args = mock_apprise_instance.notify.call_args
        assert call_args[1]["title"] == "Train Schedule 2025-12-25 14:30"
        assert "Origen: AMETZOLA - Destino: ABANDO" in call_args[1]["body"]
        assert "Train R1 available" in call_args[1]["body"]
        assert "No hay trenes disponibles" in call_args[1]["body"]

    @patch("notification_service.get_datetime")
    @patch("notification_service.Apprise")
    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken/chatid"})
    def test_send_message_multiple_messages(self, mock_apprise_class, mock_get_datetime):
        """Test send_message with multiple messages"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 10, 15)
        mock_apprise_instance = MagicMock()
        mock_apprise_class.return_value = mock_apprise_instance

        service = NotificationService()
        messages = ["Train R1 - 10:30 - 11:30 - 1h", "Train R2 - 11:00 - 12:00 - 1h", "Train R3 - 12:00 - 13:00 - 1h"]
        service.send_message(messages, "STATION_A", "STATION_B")

        call_args = mock_apprise_instance.notify.call_args
        assert call_args[1]["title"] == "Train Schedule 2025-12-25 10:15"
        assert "Origen: STATION_A - Destino: STATION_B" in call_args[1]["body"]
        for msg in messages:
            assert msg in call_args[1]["body"]

    @patch("notification_service.get_datetime")
    @patch("notification_service.Apprise")
    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken/chatid"})
    def test_send_message_empty_list(self, mock_apprise_class, mock_get_datetime):
        """Test send_message with empty list"""
        mock_get_datetime.return_value = datetime(2025, 12, 25, 10, 15)
        mock_apprise_instance = MagicMock()
        mock_apprise_class.return_value = mock_apprise_instance

        service = NotificationService()
        service.send_message([], "ORIGIN", "DESTINATION")

        call_args = mock_apprise_instance.notify.call_args
        # Empty list does not get "No hay trenes disponibles" (only lists with len==1 do)
        body = call_args[1]["body"]
        assert "Origen: ORIGIN - Destino: DESTINATION" in body

    @patch("notification_service.get_datetime")
    @patch("notification_service.Apprise")
    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken/chatid"})
    def test_send_message_format(self, mock_apprise_class, mock_get_datetime):
        """Test send_message formatting"""
        mock_get_datetime.return_value = datetime(2026, 6, 10, 8, 45)
        mock_apprise_instance = MagicMock()
        mock_apprise_class.return_value = mock_apprise_instance

        service = NotificationService()
        service.send_message(["R1 - 09:00 - 10:00 - 1h"], "BILBAO", "MADRID")

        call_args = mock_apprise_instance.notify.call_args
        body = call_args[1]["body"]

        # Check format
        assert body.startswith("Origen: BILBAO - Destino: MADRID\n")
        assert "R1 - 09:00 - 10:00 - 1h" in body
        assert "No hay trenes disponibles" in body

    @patch("notification_service.Apprise")
    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken/chatid"})
    def test_send_message_calls_notify(self, mock_apprise_class):
        """Test that send_message calls notify"""
        mock_apprise_instance = MagicMock()
        mock_apprise_class.return_value = mock_apprise_instance

        with patch("notification_service.get_datetime") as mock_get_datetime:
            mock_get_datetime.return_value = datetime(2025, 1, 1, 12, 0)

            service = NotificationService()
            service.send_message(["Test message"], "A", "B")

            # Verify notify was called exactly once
            assert mock_apprise_instance.notify.call_count == 1
