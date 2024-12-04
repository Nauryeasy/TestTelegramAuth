from django.contrib import admin

from core.apps.telegram_auth.models import TelegramUserModel

admin.site.register(TelegramUserModel)
