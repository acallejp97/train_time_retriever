# Train Schedule Bot

This project is a Telegram bot that provides train schedules. It uses the Telegram API to interact with users and fetches train schedules from an external API.

## Features

- **Start Command**: Initializes the bot.
- **Ida Command**: Searches for outbound train schedules.
- **Vuelta Command**: Searches for return train schedules.
- **Notification Service**: Sends notifications with train schedules.

## Requirements

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - `ORIGIN`: The origin station code.
    - `DESTINATION`: The destination station code.
    - `NOTIFICATION_URL`: The URL for the notification service.

## Usage

1. Run the bot:
    ```sh
    python app/bot.py
    ```

2. Interact with the bot on Telegram using the following commands:
    - `/start`: Initializes the bot.
    - `/ida`: Searches for outbound train schedules.
    - `/vuelta`: Searches for return train schedules.

## Project Structure

- `app/bot.py`: Contains the main bot logic and command handlers.
- `app/train_schedule.py`: Contains the `TrainSchedule` class for fetching train schedules.
- `app/notification_service.py`: Contains the `NotificationService` class for sending notifications.
- `app/utils.py`: Contains utility functions.

## Docker Compose Environment Variables

| Variable         | Description                          | Default Value               |
|------------------|--------------------------------------|-----------------------------|
| `CITY`           | The city for which to fetch schedules|                             |
| `ORIGIN`         | The origin station code              |                             |
| `DESTINATION`    | The destination station code         | `                           |
| `TIME_THRESHOLD` | Time threshold for schedules         | `1`                         |
| `NOTIFY`         | Notification service URL             | `tgram://<token>/<chat_id>` |
| `CRON`           | Cron schedule for running the bot    | `0 8 * * 2 - 4`             |

## License

This project is licensed under the MIT License.