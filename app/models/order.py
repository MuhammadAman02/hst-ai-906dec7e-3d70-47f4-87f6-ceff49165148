"""Order models"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, ForeignKey, DateTime, func
from datetime import datetime
from typing import List
from app.core.database import Base

class Order(Base):
    """Order model"""
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    total: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, user_id={self.user_id}, total={self.total}, status='{self.status}')>"

class OrderItem(Base):
    """Order item model"""
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Numeric(10, 2))  # Price at time of order
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    order: Mapped[Order] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
    
    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})>"
    
    @property
    def subtotal(self) -> float:
        """Calculate subtotal for this order item"""
        return float(self.price) * self.quantity