from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str

    RABBITMQ_DEFAULT_USER: str = 'guest'
    RABBITMQ_DEFAULT_PASS: str = 'guest'
    RABBITMQ_PORT: int = 5672
    RABBITMQ_MANAGEMENT_PORT: int = 15672
    RABBIT_MQ_HOST: str = 'rabbitmq'
    USER_EXCHANGE: str = 'user_exchange'
