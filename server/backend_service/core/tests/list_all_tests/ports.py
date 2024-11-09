from abc import ABC, abstractmethod
from .schemas import ListAllTestsResponse, ListAllTestsRequest

class ListAllTestsRepository(ABC):
    @abstractmethod
    def list_all_tests(self, request: ListAllTestsRequest) -> ListAllTestsResponse:
        raise NotImplementedError()
