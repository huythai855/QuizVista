from server.backend_service.core.tests.get_test_detail.ports import GetTestDetailRepository

from server.backend_service.core.tests.get_test_detail.schemas import GetTestDetailRequest, GetTestDetailResponse

from server.backend_service.infra.database.models.tests import Tests

class SQLAlchemyGetTestDetailRepository(GetTestDetailRepository):
    def __init__(self, db_session):
        self.session = db_session

    def get_test_detail(self, request: GetTestDetailRequest) -> GetTestDetailResponse:

        id = request.id
        tests = self.session.query(Tests).filter(
            Tests.id == id
        ).first()
        self.session.commit()

        if tests:
            return GetTestDetailResponse(
                message = "Get test detail successfully",
                name = tests.name,
                id = tests.id,
                description = tests.description,
                created_at = tests.created_at,
                class_id = tests.class_id,
                status = tests.status,
                created_by_id = tests.created_by_id,
                question_set = tests.question_set,
                study_note = tests.study_note,
                mindmap = tests.mindmap
            )
        else:
            return GetTestDetailResponse(
                message = "Test not found",
            )