# from server.preprocess_data.url_to_text.url_to_text import response
from .ports import ListAllMembersRepository

from .schemas import ListAllMembersResponse, ListAllMembersRequest


class ListAllMembersService:
    def __init__(self, list_all_members_repo: ListAllMembersRepository):
        self.list_all_members_repo = list_all_members_repo

    def list_all_classes(self, request: ListAllMembersRequest) -> ListAllMembersResponse:
        response = self.list_all_members_repo.list_all_members(request)
        return response