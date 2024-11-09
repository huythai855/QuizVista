from abc import ABC, abstractmethod
from .schemas import CreateNewClassRequest, CreateNewClassResponse

class CreateNewClassRepository(ABC):
    @abstractmethod
    def create_new_class(self, request: CreateNewClassRequest) -> CreateNewClassResponse:
        raise NotImplementedError()