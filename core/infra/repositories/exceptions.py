from dataclasses import dataclass


@dataclass
class TelegramUserNotFoundException(Exception):
    id: int

    def __str__(self):
        return f'Telegram user with id {self.id} not found'

    @property
    def message(self):
        return self.__str__()
