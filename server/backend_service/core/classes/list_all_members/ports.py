from abc import ABC, abstractmethod
from .schemas import ListAllMembersRequest, ListAllMembersResponse

class ListAllMembersRepository(ABC):
    @abstractmethod
    def list_all_members(self, request: ListAllMembersRequest) -> ListAllMembersResponse:
        raise NotImplementedError()
