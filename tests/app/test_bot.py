import os
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.bot import ida
from app.bot import main
from app.bot import start
from app.bot import vuelta


class TestBotHandlers:
    @pytest.mark.asyncio
    @patch("app.bot.subprocess.run")
    @patch.dict(os.environ, {"ORIGIN": "AMETZOLA", "DESTINATION": "ABANDO"})
    async def test_ida_handler(self, mock_run):
        """Test ida command handler"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await ida(mock_update, mock_context)

        # Verify message was sent
        mock_update.message.reply_text.assert_called_once_with("Buscando trenes de ida")

        # Verify subprocess was called with correct arguments
        mock_run.assert_called_once_with(["python", "main.py", "AMETZOLA", "ABANDO"])

    @pytest.mark.asyncio
    @patch("app.bot.subprocess.run")
    @patch.dict(os.environ, {"ORIGIN": "STATION_A", "DESTINATION": "STATION_B"})
    async def test_ida_handler_with_different_stations(self, mock_run):
        """Test ida handler with different station names"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await ida(mock_update, mock_context)

        mock_run.assert_called_once_with(["python", "main.py", "STATION_A", "STATION_B"])

    @pytest.mark.asyncio
    @patch("app.bot.subprocess.run")
    @patch.dict(os.environ, {"ORIGIN": "AMETZOLA", "DESTINATION": "ABANDO"})
    async def test_vuelta_handler(self, mock_run):
        """Test vuelta command handler"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await vuelta(mock_update, mock_context)

        # Verify message was sent
        mock_update.message.reply_text.assert_called_once_with("Buscando trenes de vuelta")

        # Verify subprocess was called with destination and origin swapped
        mock_run.assert_called_once_with(["python", "main.py", "ABANDO", "AMETZOLA"])

    @pytest.mark.asyncio
    @patch("app.bot.subprocess.run")
    @patch.dict(os.environ, {"ORIGIN": "STATION_A", "DESTINATION": "STATION_B"})
    async def test_vuelta_handler_with_different_stations(self, mock_run):
        """Test vuelta handler with different station names"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await vuelta(mock_update, mock_context)

        # Should swap origin and destination
        mock_run.assert_called_once_with(["python", "main.py", "STATION_B", "STATION_A"])

    @pytest.mark.asyncio
    async def test_start_handler(self):
        """Test start command handler"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await start(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once_with("Bot iniciado correctamente")

    @pytest.mark.asyncio
    @patch("app.bot.subprocess.run")
    @patch.dict(os.environ, {"ORIGIN": "A", "DESTINATION": "B"})
    async def test_ida_handler_message_type(self, mock_run):
        """Test that ida sends correct message type"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await ida(mock_update, mock_context)

        # Verify the exact message
        assert mock_update.message.reply_text.call_args[0][0] == "Buscando trenes de ida"

    @pytest.mark.asyncio
    @patch("app.bot.subprocess.run")
    @patch.dict(os.environ, {"ORIGIN": "A", "DESTINATION": "B"})
    async def test_vuelta_handler_message_type(self, mock_run):
        """Test that vuelta sends correct message type"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await vuelta(mock_update, mock_context)

        # Verify the exact message
        assert mock_update.message.reply_text.call_args[0][0] == "Buscando trenes de vuelta"

    @pytest.mark.asyncio
    async def test_start_handler_message_type(self):
        """Test that start sends correct message"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await start(mock_update, mock_context)

        assert mock_update.message.reply_text.call_args[0][0] == "Bot iniciado correctamente"

    @pytest.mark.asyncio
    @patch("app.bot.subprocess.run")
    @patch.dict(os.environ, {"ORIGIN": "AMETZOLA", "DESTINATION": "ABANDO"})
    async def test_ida_handler_subprocess_called_with_python(self, mock_run):
        """Test that ida calls subprocess with 'python' command"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await ida(mock_update, mock_context)

        # Verify first argument is "python"
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "python"
        assert call_args[1] == "main.py"

    @pytest.mark.asyncio
    @patch("app.bot.subprocess.run")
    @patch.dict(os.environ, {"ORIGIN": "AMETZOLA", "DESTINATION": "ABANDO"})
    async def test_vuelta_handler_subprocess_called_with_python(self, mock_run):
        """Test that vuelta calls subprocess with 'python' command"""
        mock_update = AsyncMock()
        mock_context = MagicMock()

        await vuelta(mock_update, mock_context)

        # Verify first argument is "python"
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "python"
        assert call_args[1] == "main.py"


class TestBotMain:
    @patch("app.bot.get_bot_token", return_value="test_token")
    @patch("app.bot.Application")
    def test_main_creates_application(self, mock_app_builder, mock_get_token):
        """Test that main() creates an Application"""
        mock_application = MagicMock()
        mock_app_builder.builder.return_value.token.return_value.build.return_value = mock_application

        main()

        # Verify Application.builder was called
        mock_app_builder.builder.assert_called_once()

    @patch("app.bot.get_bot_token", return_value="test_token")
    @patch("app.bot.Application")
    def test_main_calls_get_bot_token(self, mock_app_builder, mock_get_token):
        """Test that main() calls get_bot_token"""
        mock_application = MagicMock()
        mock_app_builder.builder.return_value.token.return_value.build.return_value = mock_application

        main()

        # Verify get_bot_token was called
        mock_get_token.assert_called_once()

    @patch("app.bot.get_bot_token", return_value="test_token")
    @patch("app.bot.Application")
    def test_main_adds_command_handlers(self, mock_app_builder, mock_get_token):
        """Test that main() adds command handlers"""
        mock_application = MagicMock()
        mock_app_builder.builder.return_value.token.return_value.build.return_value = mock_application

        main()

        # Verify add_handler was called 3 times (for start, ida, vuelta)
        assert mock_application.add_handler.call_count == 3

    @patch("app.bot.get_bot_token", return_value="test_token")
    @patch("app.bot.Application")
    def test_main_runs_polling(self, mock_app_builder, mock_get_token):
        """Test that main() runs polling"""
        mock_application = MagicMock()
        mock_app_builder.builder.return_value.token.return_value.build.return_value = mock_application

        main()

        # Verify run_polling was called with 1.0
        mock_application.run_polling.assert_called_once_with(1.0)

    @patch("app.bot.get_bot_token", return_value="test_token")
    @patch("builtins.print")
    @patch("app.bot.Application")
    def test_main_prints_listening_message(self, mock_app_builder, mock_print, mock_get_token):
        """Test that main() prints listening message"""
        mock_application = MagicMock()
        mock_app_builder.builder.return_value.token.return_value.build.return_value = mock_application

        main()

        # Verify print was called with "Listening..."
        mock_print.assert_called_with("Listening...")
