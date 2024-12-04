import punq
from django.views.generic import TemplateView

from core.project.settings.main import *

from core.application.use_cases.token import GenerateTokenUseCase
from core.project.container import get_container


class TelegramAuthView(TemplateView):
    template_name = "telegram_auth/index.html"

    def get_context_data(self, **kwargs):

        container: punq.Container = get_container()
        use_case: GenerateTokenUseCase = container.resolve(GenerateTokenUseCase)

        context = super().get_context_data(**kwargs)

        token = use_case()

        self.request.session['telegram_auth_token'] = token

        bot_username = TELEGRAM_BOT_USERNAME
        telegram_auth_url = f"https://t.me/{bot_username}?start={token}"
        context['telegram_auth_url'] = telegram_auth_url
        context['token'] = token
        return context
