import punq
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.v1.telegram_user.serializers import TelegramUserResponseSerializer
from core.application.use_cases.telegram_user import GetTelegramUserUseCase
from core.project.container import get_container


class TelegramUserView(APIView):

    def get(self, request):
        container: punq.Container = get_container()
        use_case: GetTelegramUserUseCase = container.resolve(GetTelegramUserUseCase)

        token = request.GET.get('token')
        user = use_case(token)

        if user is None:
            return Response(status=404)

        return Response(data=TelegramUserResponseSerializer(user).data, status=200)

    def post(self, request):
        pass
