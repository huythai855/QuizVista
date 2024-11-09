# from server.preprocess_data.url_to_text.url_to_text import response
from .ports import CreateNewTestRepository

from .schemas import CreateNewTestRequest, CreateNewTestResponse

class CreateNewTestService:
    def __init__(self, create_new_test_repo: CreateNewTestRepository):
        self.create_new_test_repo = create_new_test_repo

    def create_new_test(self, request: CreateNewTestRequest) -> CreateNewTestResponse:
        response = self.create_new_test_repo.create_new_test(request)
        return response
        # raise NotImplementedError()