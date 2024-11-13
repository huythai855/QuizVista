import requests
from flask import Blueprint, jsonify, request
from requests import Session

from .schemas import AddMemberRequestSchema, AddMemberResponseSchema
from ....adapter.classes.add_member import SQLAlchemyAddClassRepository
from ....core.classes.add_member.services import AddMemberService
from ....core.classes.add_member.schemas import AddMemberResponse, AddMemberRequest
from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

# from models import Base


# DATABASE_URL = "sqlite:///quizvista.db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)


sqlalchemy_config = get_sqlalchemy()

api_add_member = Blueprint('api_add_member', __name__)

@api_add_member.route("/add-member", methods=["POST"])
def add_member() -> AddMemberResponseSchema:
    body = request.get_json()
    class_info = AddMemberRequest(**body)

    db_session = sqlalchemy_config.SessionLocal()
    create_new_class_repo = SQLAlchemyAddClassRepository(db_session)
    service = AddMemberService(create_new_class_repo)

    try:
        result = service.create_new_class(class_info)
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = AddMemberResponseSchema(**result.model_dump())
    return response.model_dump()