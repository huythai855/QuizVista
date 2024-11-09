from server.backend_service.core.tests.list_all_tests.ports import ListAllTestsRepository

from server.backend_service.core.tests.list_all_tests.schemas import ListAllTestsRequest, ListAllTestsResponse, TestInfo

from server.backend_service.infra.database.models.tests import Tests

class SQLAlchemyListAllTestsRepository(ListAllTestsRepository):
    def __init__(self, db_session):
        self.session = db_session

    def list_all_tests(self, request: ListAllTestsRequest) -> ListAllTestsResponse:

        tests = self.session.query(Tests).filter().all()
        self.session.commit()

        test_list = [TestInfo(id=test.id, name=test.name, description=test.description) for test in tests]

        return ListAllTestsResponse(tests=test_list)