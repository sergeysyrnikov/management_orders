from app.interfaces.db_repository import BaseRepository
from app.models import AppUserModel


class UserRepo(BaseRepository):
    def get_by_id(self, id: int) -> AppUserModel | None:
        return self.session.query(AppUserModel).filter_by(id=id).one_or_none()

    def get_by_email(self, email: str) -> AppUserModel | None:
        return self.session.query(AppUserModel).filter_by(email=email).one_or_none()
