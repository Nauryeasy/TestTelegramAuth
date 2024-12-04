from django.contrib.auth.models import User
from django.db import models

from core.apps.telegram_auth.entities.telegram_user import TelegramUser


class TelegramUserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(unique=True)
    telegram_username = models.CharField(max_length=255, blank=True, null=True)
    telegram_first_name = models.CharField(max_length=255, blank=True, null=True)
    telegram_last_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.telegram_username or str(self.telegram_id)

    def to_entity(self):
        return TelegramUser(
            id=self.user.id,
            telegram_id=self.telegram_id,
            telegram_username=self.telegram_username,
            telegram_first_name=self.telegram_first_name,
            telegram_last_name=self.telegram_last_name
        )

    @staticmethod
    def from_entity(entity: TelegramUser):
        user, created = User.objects.get_or_create(id=entity.id)
        return TelegramUserModel(
            user=user,
            telegram_id=entity.telegram_id,
            telegram_username=entity.telegram_username,
            telegram_first_name=entity.telegram_first_name,
            telegram_last_name=entity.telegram_last_name
        )
