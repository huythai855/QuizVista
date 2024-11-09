from server.backend_service.core.classes.list_all_classes.ports import ListAllClassesRepository

from server.backend_service.core.classes.list_all_classes.schemas import ListAllClassesRequest, ListAllClassesResponse, ClassInfo

from server.backend_service.infra.database.models.classes import Classes

class SQLAlchemyListAllClassesRepository(ListAllClassesRepository):
    def __init__(self, db_session):
        self.session = db_session

    def list_all_classes(self, request: ListAllClassesRequest) -> ListAllClassesResponse:
        classes = self.session.query(Classes).filter().all()
        self.session.commit()

        class_list = [ClassInfo(
            id=each_class.id,
            name=each_class.name,
            description=each_class.description,
            created_at = each_class.created_at,
            created_by_id = each_class.created_by_id
        ) for each_class in classes]

        return ListAllClassesResponse(
            message = "List all classes successfully",
            classes = class_list
        )