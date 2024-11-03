from abc import ABC, abstractmethod
from .schemas import CreateClassRequestSchema, CreateClassResponseSchema

class ClassRepository(ABC):
    @abstractmethod
    def create(self, request: CreateClassRequestSchema) -> CreateClassResponseSchema:
        raise NotImplementedError()

    @abstractmethod
    def save_class(self, request: CreateClassRequestSchema) -> CreateClassResponseSchema:
        raise NotImplementedError()