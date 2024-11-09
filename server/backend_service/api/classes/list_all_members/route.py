from flask import Blueprint, request, jsonify

from server.backend_service.api.classes.list_all_members.schemas import (
    ListAllMembersResponseSchema,
    ListAllMembersRequestSchema
)

from server.backend_service.core.classes.list_all_members.schemas import (
    ListAllMembersResponse,
    ListAllMembersRequest
)

from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

from ....adapter.classes.list_all_members import SQLAlchemyListAllMembersRepository
from ....core.classes.list_all_members.services import ListAllMembersService

sqlalchemy_config = get_sqlalchemy()

api_list_all_members = Blueprint('api_list_all_members', __name__)


@api_list_all_members.route("/members", methods=["GET"])
def list_all_members() -> ListAllMembersResponseSchema:

    db_session = sqlalchemy_config.SessionLocal()
    list_all_members_repo = SQLAlchemyListAllMembersRepository(db_session)
    service = ListAllMembersService(list_all_members_repo)

    class_id = request.args.get('class_id')

    try:
        result = service.list_all_classes(ListAllMembersRequest(class_id=class_id))
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = ListAllMembersResponseSchema(**result.model_dump())

    return response.model_dump()
