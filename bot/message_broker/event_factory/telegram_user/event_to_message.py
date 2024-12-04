from domain.events.telegram_user import TelegramUserCreatedEvent


def telegram_user_created_event_to_message(event: TelegramUserCreatedEvent) -> dict:
    return {
        'oid': event.oid,
        'type': event.__class__.__name__,
        'created_at': str(event.created_at),
        'data': {
            'telegram_id': event.telegram_id,
            'telegram_username': event.telegram_username,
            'telegram_first_name': event.telegram_first_name,
            'telegram_last_name': event.telegram_last_name,
            'token': event.token
        }
    }
