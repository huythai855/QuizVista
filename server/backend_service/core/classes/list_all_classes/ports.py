from abc import ABC, abstractmethod
from .schemas import ListAllClassesRequest, ListAllClassesResponse

class ListAllClassesRepository(ABC):
    @abstractmethod
    def list_all_classes(self, request: ListAllClassesRequest) -> ListAllClassesResponse:
        raise NotImplementedError()
