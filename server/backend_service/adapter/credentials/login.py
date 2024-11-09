from server.backend_service.core.credentials.login.ports import LoginRepository
from ...core.credentials.login.schemas import LoginResponse
from ...infra.database.models.users import Users

class SQLAlchemyLoginRepository(LoginRepository):
    def __init__(self, db_session):
        self.session = db_session

    def validate_login(self, request):

        # self.session.query(User).filter(User.email == request.email).first()

        username = request.username
        password = request.password


        response = self.session.query(Users).filter(
            Users.username == username,
            Users.password == password
        ).first()


        if response is None:
            return LoginResponse(
                message = "Login unsuccessfully",
            )
        else:
            return LoginResponse(
                message = "Login successfully",
                username = response.username,
                user_id = response.id,
                fullname = response.fullname
            )