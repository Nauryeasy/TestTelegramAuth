from dataclasses import dataclass

from django.contrib.auth.models import User

from core.apps.telegram_auth.entities.telegram_user import TelegramUser
from core.apps.telegram_auth.models import TelegramUserModel
from core.infra.repositories.base import BaseTelegramUserRepository
from core.infra.repositories.exceptions import TelegramUserNotFoundException


@dataclass
class TelegramUserRepository(BaseTelegramUserRepository):
    def get_by_id(self, telegram_id: int) -> TelegramUser:
        try:
            telegram_user_model_object = TelegramUserModel.objects.get(telegram_id=str(telegram_id))
        except TelegramUserModel.DoesNotExist:
            raise TelegramUserNotFoundException(id=telegram_id)

        return telegram_user_model_object.to_entity()

    def create(self, entity: TelegramUser) -> TelegramUser:
        telegram_user_model_object = TelegramUserModel.from_entity(entity)

        telegram_user_model_object.save()

        return telegram_user_model_object.to_entity()

    def check_exists(self, entity: TelegramUser) -> bool:
        try:
            TelegramUserModel.objects.get(telegram_id=entity.telegram_id)
            return True
        except TelegramUserModel.DoesNotExist:
            return False
