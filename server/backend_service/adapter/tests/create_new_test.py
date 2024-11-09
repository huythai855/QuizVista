from server.backend_service.core.tests.create_new_test.ports import CreateNewTestRepository

from server.backend_service.core.tests.create_new_test.schemas import CreateNewTestRequest, CreateNewTestResponse

from server.backend_service.infra.database.models.tests import Tests

class SQLAlchemyCreateNewTestRepository(CreateNewTestRepository):
    def __init__(self, db_session):
        self.session = db_session

    def create_new_test(self, request: CreateNewTestRequest) -> CreateNewTestResponse:

        count_test = self.session.query(Tests).filter().count()

        new_test = Tests(
            id = count_test + 1,
            name = request.name,
            description= request.description,
            created_at= request.created_at,
            class_id= request.class_id,
            status= request.status,
            created_by_id= request.created_by_id,
            question_set= request.question_set,
            study_note= request.study_note,
            mindmap= request.mindmap
        )

        self.session.add(new_test)
        self.session.commit()

        return CreateNewTestResponse(
            message = "User created successfully",
            name = new_test.name,
            id = new_test.id,
            description = new_test.description
       )