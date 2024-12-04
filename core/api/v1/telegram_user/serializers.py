from rest_framework import serializers


class TelegramUserResponseSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    telegram_username = serializers.CharField()
    telegram_first_name = serializers.CharField()
    telegram_last_name = serializers.CharField()
