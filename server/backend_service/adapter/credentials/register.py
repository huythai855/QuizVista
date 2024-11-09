from server.backend_service.core.credentials.register.ports import RegisterRepository

from server.backend_service.core.credentials.register.schemas import RegisterRequest, RegisterResponse

from server.backend_service.infra.database.models.users import Users

class SQLAlchemyRegisterRepository(RegisterRepository):
    def __init__(self, db_session):
        self.session = db_session

    def create_user(self, request: RegisterRequest) -> RegisterResponse:

        count_user = self.session.query(Users).filter().count()

        user = Users(
            id = count_user + 1,
            username = request.username,
            password = request.password,
            role= request.role,
            registered_at= request.registered_at,
            fullname = request.fullname,
            gender=request.gender,
            dob=request.dob,
        )

        self.session.add(user)
        self.session.commit()

        return RegisterResponse(
            message = "User created successfully",
            username = user.username,
            user_id = user.id,
            fullname = user.fullname
       )