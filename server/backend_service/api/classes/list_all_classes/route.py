from flask import Blueprint, request, jsonify

from server.backend_service.api.classes.list_all_classes.schemas import (
    ListAllClassesResponseSchema,
    ListAllClassesRequestSchema
)

from server.backend_service.core.classes.list_all_classes.schemas import (
    ListAllClassesResponse,
    ListAllClassesRequest
)

from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

from ....adapter.classes.list_all_classes import SQLAlchemyListAllClassesRepository
from ....core.classes.list_all_classes.services import ListAllClassesService

sqlalchemy_config = get_sqlalchemy()

api_list_all_classes = Blueprint('api_list_all_classes', __name__)


@api_list_all_classes.route("/", methods=["GET"])
def list_all_tests() -> ListAllClassesResponseSchema:

    db_session = sqlalchemy_config.SessionLocal()
    create_new_test_repo = SQLAlchemyListAllClassesRepository(db_session)
    service = ListAllClassesService(create_new_test_repo)

    try:
        result = service.list_all_classes(ListAllClassesRequest())
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = ListAllClassesResponseSchema(**result.model_dump())

    return response.model_dump()
