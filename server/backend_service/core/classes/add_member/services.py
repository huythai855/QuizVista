from .ports import AddMemberRepository

from .schemas import AddMemberResponse, AddMemberRequest

class AddMemberService:
    def __init__(self, add_member_repo: AddMemberRepository):
        self.add_member_repo = add_member_repo

    def create_new_class(self, request: AddMemberRequest) -> AddMemberResponse:
        add_member_request = self.add_member_repo.add_member(request)

        response = AddMemberResponse(
            message = add_member_request.message,
        )

        return response
