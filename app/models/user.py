from sqlalchemy import (
    Column,
    Integer,
    String,
    func,
    DateTime,
    SmallInteger,
    Boolean,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from app.models import BaseModel


class AppUserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), unique=True, nullable=False)
    username = Column(String(128), unique=True)
    hashed_password = Column(String(255), nullable=False)
    age = Column(SmallInteger)
    gender = Column(Boolean)
    role = Column(String(32), nullable=False, server_default="user", index=True)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    orders = relationship("OrderModel", back_populates="user", lazy="selectin")

    __table_args__ = (
        CheckConstraint(
            "age > 0 AND age < 150",
            name="check_users_age_range",
        ),
    )

    def __repr__(self):
        return f"<User: {self.email}>"
