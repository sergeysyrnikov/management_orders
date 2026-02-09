import enum
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    UUID,
    DECIMAL,
    CheckConstraint,
    text,
    Index,
    Enum,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models import BaseModel


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"


class OrderModel(BaseModel):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    items = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    total_price = Column(DECIMAL(10, 2), server_default=text("0"))
    status = Column(
        Enum(OrderStatus, name="order_status"),
        nullable=False,
        server_default=OrderStatus.PENDING.value,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("AppUserModel", back_populates="orders")

    __table_args__ = (
        CheckConstraint("total_price >= 0", name="check_orders_total_price"),
        Index("idx_orders_user_status", "user_id", "status"),
    )

    def __repr__(self):
        return f"<Order {self.id}, user_id: {self.user_id}>"
