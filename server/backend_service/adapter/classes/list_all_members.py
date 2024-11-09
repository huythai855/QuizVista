from sqlalchemy.orm import joinedload
from server.backend_service.core.classes.list_all_members.ports import ListAllMembersRepository

from server.backend_service.core.classes.list_all_members.schemas import ListAllMembersResponse, ListAllMembersRequest, ClassJoinInfo

from server.backend_service.infra.database.models.class_join import ClassJoin
from server.backend_service.infra.database.models.users import Users


class SQLAlchemyListAllMembersRepository(ListAllMembersRepository):
    def __init__(self, db_session):
        self.session = db_session

    def list_all_members(self, request: ListAllMembersRequest) -> ListAllMembersResponse:
        classes = (
            self.session.query(ClassJoin, Users.fullname)
            .join(Users, ClassJoin.joined_by_id == Users.id)
            .all()
        )

        # classes = self.session.query(Join(ClassJoin, Users)).filter().all()
        self.session.commit()

        class_joint = [ClassJoinInfo(
            id=each_class_joint.ClassJoin.id,
            class_id=each_class_joint.ClassJoin.class_id,
            joined_by_id=each_class_joint.ClassJoin.joined_by_id,
            fullname = each_class_joint.fullname,
            role = each_class_joint.ClassJoin.role
        ) for each_class_joint in classes]

        return ListAllMembersResponse(
            members = class_joint
        )