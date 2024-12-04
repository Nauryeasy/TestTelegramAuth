from core.apps.telegram_auth.events.telegram_user import TelegramUserCreatedEvent


def telegram_user_created_message_to_event(message: dict) -> TelegramUserCreatedEvent:
    return TelegramUserCreatedEvent(
        oid=message['oid'],
        created_at=message['created_at'],
        token=message['data']['token'],
        telegram_id=message['data']['telegram_id'],
        telegram_username=message['data']['telegram_username'],
        telegram_first_name=message['data']['telegram_first_name'],
        telegram_last_name=message['data']['telegram_last_name'],
    )
