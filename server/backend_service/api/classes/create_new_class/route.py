import requests
from flask import Blueprint, jsonify, request
from requests import Session

from .schemas import CreateNewClassRequestSchema, CreateNewClassResponseSchema
from ....adapter.classes.create_new_class import SQLAlchemyCreateNewClassRepository
from ....core.classes.create_new_class.services import CreateNewClassService
from ....core.classes.create_new_class.schemas import CreateNewClassRequest, CreateNewClassResponse
from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

# from models import Base


# DATABASE_URL = "sqlite:///quizvista.db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)


sqlalchemy_config = get_sqlalchemy()

api_create_classes = Blueprint('api_create_class', __name__)

@api_create_classes.route("/", methods=["POST"])
def create_new_class() -> CreateNewClassResponseSchema:
    body = request.get_json()
    class_info = CreateNewClassRequest(**body)

    db_session = sqlalchemy_config.SessionLocal()
    create_new_class_repo = SQLAlchemyCreateNewClassRepository(db_session)
    service = CreateNewClassService(create_new_class_repo)

    try:
        result = service.create_new_class(class_info)
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = CreateNewClassResponseSchema(**result.model_dump())
    return response.model_dump()