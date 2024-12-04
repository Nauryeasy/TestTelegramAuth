import uuid
from dataclasses import dataclass

from core.application.use_cases.base import BaseUseCase


@dataclass
class GenerateTokenUseCase(BaseUseCase):

    def __call__(self, *args, **kwargs):
        import secrets
        return secrets.token_urlsafe(16)
