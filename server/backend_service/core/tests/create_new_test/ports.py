from abc import ABC, abstractmethod
from .schemas import CreateNewTestRequest, CreateNewTestResponse

class CreateNewTestRepository(ABC):
    @abstractmethod
    def create_new_test(self, request: CreateNewTestRequest) -> CreateNewTestResponse:
        raise NotImplementedError()
