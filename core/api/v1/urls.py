from django.urls import path

from core.api.v1.telegram_user.views import TelegramUserView

urlpatterns = [
    path('telegram_user/', TelegramUserView.as_view()),
]