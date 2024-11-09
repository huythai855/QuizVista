from sqlalchemy.orm import Session
from ...core.classes.create_new_class.ports import CreateNewClassRepository
from ...core.classes.create_new_class.schemas import CreateNewClassResponse
from ...infra.database.models.classes import Classes

class SQLAlchemyCreateNewClassRepository(CreateNewClassRepository):
    def __init__(self, db_session: Session):
        self.session = db_session

    def create_new_class(self, request):
        new_class_request = request.model_dump()

        count_class = self.session.query(Classes).filter().count()

        new_class = Classes(
            id = count_class + 1,
            name = new_class_request['name'],
            description = new_class_request['description'],
            created_at = new_class_request['created_at'],
            created_by_id = new_class_request['created_by_id'],
        )

        self.session.add(new_class)
        self.session.commit()

        return CreateNewClassResponse(
            message = "Class created successfully",
            id = new_class.id,
            name = new_class.name,
            description = new_class.description,
            created_at = new_class.created_at,
            created_by_id = new_class.created_by_id,
        )
