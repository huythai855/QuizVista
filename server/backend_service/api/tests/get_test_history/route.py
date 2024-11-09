from flask import Blueprint, request, jsonify

from server.backend_service.api.tests.get_test_history.schemas import (
    GetTestHistoryRequestSchema,
    GetTestHistoryResponseSchema
)

from server.backend_service.core.tests.get_test_history.schemas import (
    GetTestHistoryResponse,
    GetTestHistoryRequest
)

from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

from ....adapter.tests.get_test_history import SQLAlchemyGetTestHistoryRepository
# from ....adapter.tests.list_all_tests import SQLAlchemyListAllTestsRepository
from ....core.tests.get_test_history.services import GetTestHistoryService

sqlalchemy_config = get_sqlalchemy()

api_get_test_history = Blueprint('api_get_test_history', __name__)


@api_get_test_history.route("/history", methods=["GET"])
def get_test_history() -> GetTestHistoryResponseSchema:
    test_id = request.args.get('test_id')

    db_session = sqlalchemy_config.SessionLocal()
    get_test_history_repo = SQLAlchemyGetTestHistoryRepository(db_session)
    service = GetTestHistoryService(get_test_history_repo)

    try:
        result = service.get_test_history(GetTestHistoryRequest(test_id=test_id))
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = GetTestHistoryResponseSchema(**result.model_dump())

    return response.model_dump()
