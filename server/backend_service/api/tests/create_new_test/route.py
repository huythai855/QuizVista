import requests
from flask import Blueprint, request, jsonify

from server.backend_service.api.tests.create_new_test.schemas import (
    CreateNewTestRequestSchema,
    CreateNewTestResponseSchema
)

from server.backend_service.core.tests.create_new_test.schemas import (
    CreateNewTestResponse,
    CreateNewTestRequest
)

from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

from ....adapter.tests.create_new_test import SQLAlchemyCreateNewTestRepository
from ....core.tests.create_new_test.services import CreateNewTestService

sqlalchemy_config = get_sqlalchemy()

api_create_new_test = Blueprint('api_create_new_test', __name__)


@api_create_new_test.route("/", methods=["POST"])
def register() -> CreateNewTestResponseSchema:

    body = request.get_json()
    new_test_info = CreateNewTestRequest(**body)

    db_session = sqlalchemy_config.SessionLocal()
    create_new_test_repo = SQLAlchemyCreateNewTestRepository(db_session)
    service = CreateNewTestService(create_new_test_repo)

    try:
        result = service.create_new_test(new_test_info)
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = CreateNewTestResponseSchema(**result.model_dump())

    return response.model_dump()
