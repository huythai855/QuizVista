from types import new_class

from sqlalchemy.orm import Session
from ...core.classes.create_class.ports import ClassRepository
from ...infra.database.models.classes import Classes as ClassesModel

class SQLAlchemyClassRepository(ClassRepository):
    def __init__(self, db_session: Session):
        self.session = db_session

    def create(self, request):
        # TODO: Implement logic luu vao db o day
        pass

    def save_class(self, request):
        new_class_request = request.model_dump()
        print("New class:", new_class_request)

        new_class = ClassesModel(
            id = new_class_request['id'],
            name = new_class_request['name'],
            description = new_class_request['description'],
        )


        self.session.add(new_class)
        self.session.commit()
        return new_class