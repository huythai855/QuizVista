from .ports import ClassRepository

# from server.backend_service.api.classes.create_class.route import create_class
from server.backend_service.core.classes.create_class.schemas import CreateClassRequestSchema, CreateClassResponseSchema


class CreateClassService:
    def __init__(self, create_class_port: ClassRepository):
        self.create_class_port = create_class_port

    def create(self, request: CreateClassRequestSchema) -> CreateClassResponseSchema:
        created_class = self.create_class_port.save_class(request)

        print(created_class)

        response = CreateClassResponseSchema(
            id = created_class.id,
            name = created_class.name,
            description = created_class.description,

            # updated_at = created_class.updated_at,
            # created_at = create_class.created_at
        )

        return response
