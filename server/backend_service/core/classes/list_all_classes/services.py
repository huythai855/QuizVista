# from server.preprocess_data.url_to_text.url_to_text import response
from .ports import ListAllClassesRepository

from .schemas import ListAllClassesResponse, ListAllClassesRequest

class ListAllClassesService:
    def __init__(self, list_all_classes_repo: ListAllClassesRepository):
        self.list_all_classes_repo = list_all_classes_repo

    def list_all_classes(self, request: ListAllClassesRequest) -> ListAllClassesResponse:
        response = self.list_all_classes_repo.list_all_classes(request)
        return response