from .ports import LoginRepository

from .schemas import LoginRequest, LoginResponse

class LoginService:
    def __init__(self, login_repository: LoginRepository):
        self.login_repository = login_repository

    def login(self, request: LoginRequest) -> LoginResponse:
        validate = self.login_repository.validate_login(request)
        response = LoginResponse(**validate.dict())
        return response