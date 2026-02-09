from sqlalchemy.exc import NoResultFound

from app.interfaces import BaseService
from app.models import AppUserModel
from app.repositories.user import UserRepo
from app.utils.user import verify_password


class VerifyError(Exception):
    pass


class UserService(BaseService):
    def __init__(self, session):
        super().__init__(session)
        self.user_repo = UserRepo(session)

    def verify_by_email_pwd(
        self, email: str, password: str
    ) -> tuple[bool, Exception | AppUserModel]:
        user = self.user_repo.get_by_email(email)
        if user is None:
            return False, NoResultFound("User with this email does not exist")
        if not verify_password(password, user.hashed_password):
            return False, VerifyError("User verify error")
        return True, user
