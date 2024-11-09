# from server.preprocess_data.url_to_text.url_to_text import response
from .ports import ListAllTestsRepository

from .schemas import ListAllTestsResponse, ListAllTestsRequest

class ListAllTestsService:
    def __init__(self, list_all_tests_repo: ListAllTestsRepository):
        self.list_all_tests_repo = list_all_tests_repo

    def list_all_tests(self, request: ListAllTestsRequest) -> ListAllTestsResponse:
        response = self.list_all_tests_repo.list_all_tests(request)
        return response