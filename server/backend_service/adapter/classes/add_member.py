from sqlalchemy.orm import Session
from ...core.classes.add_member.ports import AddMemberRepository
from ...core.classes.add_member.schemas import AddMemberResponse
from ...infra.database.models.class_join import ClassJoin

class SQLAlchemyAddClassRepository(AddMemberRepository):
    def __init__(self, db_session: Session):
        self.session = db_session

    def add_member(self, request):
        new_member_request = request.model_dump()
        count_class_join = self.session.query(ClassJoin).filter().count()

        new_member = ClassJoin(
            id = count_class_join + 1,
            class_id= new_member_request['class_id'],
            joined_by_id = new_member_request['user_id'],
            role = new_member_request['role'],
        )

        self.session.add(new_member)
        self.session.commit()

        return AddMemberResponse(
            message = "Added member to class successfully",
        )
