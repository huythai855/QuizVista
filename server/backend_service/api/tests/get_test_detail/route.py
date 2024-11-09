from flask import Blueprint, request, jsonify

from server.backend_service.api.tests.get_test_detail.schemas import (
    GetTestDetailResponseSchema,
    GetTestDetailRequestSchema
)

from server.backend_service.core.tests.get_test_detail.schemas import (
    GetTestDetailRequest,
    GetTestDetailResponse
)

from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

from ....adapter.tests.get_test_detail import SQLAlchemyGetTestDetailRepository
from ....core.tests.get_test_detail.services import GetTestDetailService

sqlalchemy_config = get_sqlalchemy()

api_get_test_detail = Blueprint('api_get_test_detail', __name__)


@api_get_test_detail.route("/detail", methods=["GET"])
def get_test_detail() -> GetTestDetailResponseSchema:

    # body = request.get_json()
    # new_test_info = ListAllTestsRequest(**body)

    test_id = request.args.get('test_id')
    db_session = sqlalchemy_config.SessionLocal()
    get_test_detail_repo = SQLAlchemyGetTestDetailRepository(db_session)
    service = GetTestDetailService(get_test_detail_repo)

    try:
        result = service.get_test_detail(GetTestDetailRequest(id=test_id))
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = GetTestDetailResponseSchema(**result.model_dump())

    return response.model_dump()
