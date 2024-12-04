from django.urls import path

from core.frontend.views import TelegramAuthView

urlpatterns = [
    path('', TelegramAuthView.as_view()),
]
