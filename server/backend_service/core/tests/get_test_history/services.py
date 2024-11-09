# from server.preprocess_data.url_to_text.url_to_text import response
from .ports import GetTestHistoryRepository

from .schemas import GetTestHistoryResponse, GetTestHistoryRequest, TestHistory

class GetTestHistoryService:
    def __init__(self, get_test_history_repo: GetTestHistoryRepository):
        self.get_test_history_repo = get_test_history_repo

    def get_test_history(self, request: GetTestHistoryRequest) -> GetTestHistoryResponse:
        response = self.get_test_history_repo.get_test_history(request)
        return response