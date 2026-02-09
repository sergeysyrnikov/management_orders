from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class BaseRepository(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_by_id(self, id: int) -> Any | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Any | None:
        pass
