# from server.preprocess_data.url_to_text.url_to_text import response
from .ports import GetTestDetailRepository

from .schemas import GetTestDetailRequest, GetTestDetailResponse

class GetTestDetailService:
    def __init__(self, get_test_detail_repo: GetTestDetailRepository):
        self.get_test_detail_repo = get_test_detail_repo

    def get_test_detail(self, request: GetTestDetailRequest) -> GetTestDetailResponse:
        response = self.get_test_detail_repo.get_test_detail(request)
        return response