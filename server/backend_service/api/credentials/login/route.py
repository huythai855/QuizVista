from flask import Blueprint, request, jsonify

from server.backend_service.api.credentials.login.schemas import (
    LoginResponseSchema,
    LoginRequestSchema
)

from server.backend_service.core.credentials.login.schemas import (
    LoginResponse,
    LoginRequest
)

from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

from ....adapter.credentials.login import SQLAlchemyLoginRepository
from ....core.credentials.login.services import LoginService

sqlalchemy_config = get_sqlalchemy()

api_login = Blueprint('api_login', __name__)


@api_login.route("/login", methods=["POST"])
def login() -> LoginResponseSchema:

    body = request.get_json()
    login_info = LoginRequest(**body)

    db_session = sqlalchemy_config.SessionLocal()
    login_repo = SQLAlchemyLoginRepository(db_session)
    service = LoginService(login_repo)

    try:
        result = service.login(login_info)
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = LoginResponseSchema(**result.model_dump())
    return response.model_dump()
