import requests
from flask import Blueprint, jsonify, request
from requests import Session

from .schemas import CreateClassRequestSchema, CreateClassResponseSchema
from ....adapter.classes.create_class import SQLAlchemyClassRepository
from ....core.classes.create_class.services import CreateClassService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy

# from models import Base


# DATABASE_URL = "sqlite:///quizvista.db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)


sqlalchemy_config = get_sqlalchemy()



api_create_classes = Blueprint('api', __name__)

# TODO: Maybe không cần dùng async/await
@api_create_classes.route("/create", methods=["POST"])
def create_class(
        # user_id: str,
        # body: CreateClassRequestSchema
    ) -> CreateClassResponseSchema:

    user_id = request.args.get('user_id')
    body = request.get_json()

    print(user_id)
    print(body)

    create_class = CreateClassRequestSchema(**body)

    db_session = sqlalchemy_config.SessionLocal()
    class_repo = SQLAlchemyClassRepository(db_session)
    service = CreateClassService(class_repo)

    try:
        result = service.create(create_class)
    except ValueError as e:
        raise ValueError(e)
    finally:
        db_session.close()

    response = CreateClassResponseSchema(**result.model_dump())
    return jsonify(response.model_dump()), 201