from flask import Blueprint, request, jsonify

from server.backend_service.api.tests.list_all_tests.schemas import (
    ListAllTestsRequestSchema,
    ListAllTestsResponseSchema
)

from server.backend_service.core.tests.list_all_tests.schemas import (
    ListAllTestsRequest,
    ListAllTestsResponse
)

from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

from ....adapter.tests.list_all_tests import SQLAlchemyListAllTestsRepository
from ....core.tests.list_all_tests.services import ListAllTestsService

sqlalchemy_config = get_sqlalchemy()

api_list_all_tests = Blueprint('api_list_all_tests', __name__)


@api_list_all_tests.route("/", methods=["GET"])
def list_all_tests() -> ListAllTestsResponseSchema:

    db_session = sqlalchemy_config.SessionLocal()
    list_all_tests_repo = SQLAlchemyListAllTestsRepository(db_session)
    service = ListAllTestsService(list_all_tests_repo)

    try:
        result = service.list_all_tests(ListAllTestsRequest())
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = ListAllTestsResponseSchema(**result.model_dump())

    return response.model_dump()