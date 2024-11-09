from abc import ABC, abstractmethod
from .schemas import LoginRequest, LoginResponse

class LoginRepository(ABC):
    @abstractmethod
    def validate_login(self, request: LoginRequest) -> LoginResponse:
        raise NotImplementedError()