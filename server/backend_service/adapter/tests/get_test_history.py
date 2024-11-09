from server.backend_service.core.tests.get_test_history.ports import GetTestHistoryRepository

from server.backend_service.core.tests.get_test_history.schemas import GetTestHistoryRequest, GetTestHistoryResponse, TestHistory

from server.backend_service.infra.database.models.test_taken import TestTaken

class SQLAlchemyGetTestHistoryRepository(GetTestHistoryRepository):
    def __init__(self, db_session):
        self.session = db_session

    def get_test_history(self, request: GetTestHistoryRequest) -> GetTestHistoryResponse:
        test_id =  request.test_id

        test_taken = self.session.query(TestTaken).filter(
            TestTaken.exam_id == test_id
        ).all()

        self.session.commit()

        test_list = [TestHistory(
            id=test.id,
            exam_id=test.exam_id,
            taken_by_id=test.taken_by_id,
            taken_date=test.taken_date,
            score=test.score
        ) for test in test_taken]


        if test_list:
            return GetTestHistoryResponse(
                message="Test taken found",
                test_taken=test_list
            )
        else:
            return GetTestHistoryResponse(
                message="No test taken found",
                test_taken=[]
            )
