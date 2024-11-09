from abc import ABC, abstractmethod
from .schemas import GetTestDetailRequest, GetTestDetailResponse

class GetTestDetailRepository(ABC):
    @abstractmethod
    def get_test_detail(self, request: GetTestDetailRequest) -> GetTestDetailResponse:
        raise NotImplementedError()
