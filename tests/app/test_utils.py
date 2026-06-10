import os
from datetime import datetime
from unittest.mock import patch

import pytest

from utils import as_time
from utils import get_bot_token
from utils import get_datetime
from utils import get_time


class TestGetDatetime:
    def test_get_datetime_returns_datetime_object(self):
        """Test that get_datetime returns a datetime object"""
        result = get_datetime()
        assert isinstance(result, datetime)

    def test_get_datetime_returns_current_time(self):
        """Test that get_datetime returns approximately current time"""
        before = datetime.now()
        result = get_datetime()
        after = datetime.now()
        assert before <= result <= after


class TestGetTime:
    def test_get_time_returns_string_in_hh_mm_format(self):
        """Test that get_time returns a string in HH:MM format"""
        result = get_time()
        assert isinstance(result, str)
        assert len(result) == 5
        assert result[2] == ":"

    def test_get_time_format(self):
        """Test that get_time format is valid"""
        result = get_time()
        # Should not raise exception
        datetime.strptime(result, "%H:%M")

    @patch("utils.get_datetime")
    def test_get_time_with_mocked_datetime(self, mock_datetime):
        """Test get_time with mocked datetime"""
        mock_datetime.return_value = datetime(2025, 12, 25, 14, 30)
        result = get_time()
        assert result == "14:30"


class TestAsTime:
    def test_as_time_converts_string_to_datetime(self):
        """Test that as_time converts a string to datetime object"""
        result = as_time("14:30")
        assert isinstance(result, datetime)

    def test_as_time_correct_conversion(self):
        """Test that as_time converts correctly"""
        result = as_time("14:30")
        expected = datetime.strptime("14:30", "%H:%M")
        assert result == expected

    def test_as_time_midnight(self):
        """Test as_time with midnight"""
        result = as_time("00:00")
        assert result.hour == 0
        assert result.minute == 0

    def test_as_time_invalid_format(self):
        """Test as_time with invalid format raises error"""
        with pytest.raises(ValueError):
            as_time("14-30")

    def test_as_time_comparison(self):
        """Test that as_time results can be compared"""
        time1 = as_time("10:30")
        time2 = as_time("14:30")
        assert time1 < time2


class TestGetBotToken:
    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken123/chatid456"})
    def test_get_bot_token_extracts_token_correctly(self):
        """Test that get_bot_token extracts token from URL (second-to-last part)"""
        result = get_bot_token()
        # Returns the second-to-last part of the split URL (index -2)
        assert result == "bottoken123"

    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken/chatid"})
    def test_get_bot_token_returns_second_last_part_of_url(self):
        """Test that get_bot_token returns second-to-last part of URL"""
        result = get_bot_token()
        # Returns the second-to-last part after split
        assert result == "bottoken"

    @patch.dict(os.environ, {}, clear=True)
    def test_get_bot_token_raises_when_notification_url_is_none(self):
        """Test that get_bot_token raises ValueError when NOTIFICATION_URL is not set"""
        # When NOTIFICATION_URL is not set, it defaults to "None"
        with pytest.raises(ValueError, match="Token not found"):
            get_bot_token()

    @patch.dict(os.environ, {"NOTIFICATION_URL": "None"})
    def test_get_bot_token_raises_when_notification_url_value_is_none(self):
        """Test that get_bot_token raises ValueError when NOTIFICATION_URL value is 'None'"""
        with pytest.raises(ValueError, match="Token not found"):
            get_bot_token()

    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bot123/chatid/extra/data"})
    def test_get_bot_token_with_multiple_slashes(self):
        """Test get_bot_token with multiple slashes in URL (returns second-to-last)"""
        result = get_bot_token()
        # Returns second-to-last element from split
        assert result == "extra"

    @patch.dict(os.environ, {"NOTIFICATION_URL": "tg://bottoken/chatid/extra"})
    def test_get_bot_token_with_three_parts(self):
        """Test get_bot_token with three path segments"""
        result = get_bot_token()
        assert result == "chatid"
