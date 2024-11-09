from abc import ABC, abstractmethod
from .schemas import GetTestHistoryRequest, GetTestHistoryResponse

class GetTestHistoryRepository(ABC):
    @abstractmethod
    def get_test_history(self, request: GetTestHistoryRequest) -> GetTestHistoryResponse:
        raise NotImplementedError()
