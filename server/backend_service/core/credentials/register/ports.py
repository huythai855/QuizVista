from abc import ABC, abstractmethod
from .schemas import RegisterRequest, RegisterResponse

class RegisterRepository(ABC):
    @abstractmethod
    def create_user(self, request: RegisterRequest) -> RegisterResponse:
        raise NotImplementedError()