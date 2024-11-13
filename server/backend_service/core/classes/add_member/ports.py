from abc import ABC, abstractmethod
from .schemas import AddMemberRequest, AddMemberResponse

class AddMemberRepository(ABC):
    @abstractmethod
    def add_member(self, request: AddMemberRequest) -> AddMemberResponse:
        raise NotImplementedError()