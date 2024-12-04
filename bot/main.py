import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from container import get_container
from domain.events.telegram_user import TelegramUserCreatedEvent
from message_broker.producer.rabbit_mq_producer import UserRabbitMQProducer
from settings import Settings

container = get_container()
settings: Settings = container.resolve(Settings)

TELEGRAM_API_TOKEN = settings.TOKEN

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    token = message.text.split()[-1]
    if not token:
        await message.reply("Привет! Токен не найден. Обратитесь к администратору.")
        return

    event = TelegramUserCreatedEvent(
        token=token,
        telegram_id=message.from_user.id,
        telegram_username=message.from_user.username,
        telegram_first_name=message.from_user.first_name,
        telegram_last_name=message.from_user.last_name,
    )

    producer: UserRabbitMQProducer = container.resolve(UserRabbitMQProducer)

    producer.publish(event)

    await message.reply(
        f"Спасибо, {message.from_user.first_name}! Ваш токен успешно зарегистрирован."
    )


async def main() -> None:
    bot = Bot(token=TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
