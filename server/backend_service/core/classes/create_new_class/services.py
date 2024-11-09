from .ports import CreateNewClassRepository

from .schemas import CreateNewClassRequest, CreateNewClassResponse

class CreateNewClassService:
    def __init__(self, create_new_class_repo: CreateNewClassRepository):
        self.create_new_class_repo = create_new_class_repo

    def create_new_class(self, request: CreateNewClassRequest) -> CreateNewClassResponse:
        created_class = self.create_new_class_repo.create_new_class(request)

        response = CreateNewClassResponse(
            message = created_class.message,
            id = created_class.id,
            name = created_class.name,
            description = created_class.description,
            created_at = created_class.created_at,
            created_by_id = created_class.created_by_id,
        )

        return response
