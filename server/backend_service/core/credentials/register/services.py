from .ports import RegisterRepository
from .schemas import RegisterRequest, RegisterResponse

class RegisterService:
    def __init__(self, register_repository: RegisterRepository):
        self.register_repository = register_repository

    def create_user(self, request: RegisterRequest) -> RegisterResponse:
        response = self.register_repository.create_user(request)
        return response