from flask import Blueprint, request, jsonify

from server.backend_service.api.credentials.register.schemas import (
    RegisterResponseSchema,
    RegisterRequestSchema
)

from server.backend_service.core.credentials.register.schemas import (
    RegisterResponse,
    RegisterRequest
)

from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

from ....adapter.credentials.register import SQLAlchemyRegisterRepository
from ....core.credentials.register.services import RegisterService

sqlalchemy_config = get_sqlalchemy()

api_register = Blueprint('api_register', __name__)


@api_register.route("/register", methods=["POST"])
def register() -> RegisterResponseSchema:

    body = request.get_json()
    register_info = RegisterRequest(**body)

    db_session = sqlalchemy_config.SessionLocal()
    register_repo = SQLAlchemyRegisterRepository(db_session)
    service = RegisterService(register_repo)

    try:
        result = service.create_user(register_info)
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = RegisterResponseSchema(**result.model_dump())
    return response.model_dump()
