"""Shopping cart models"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, func
from datetime import datetime
from typing import List
from app.core.database import Base

class Cart(Base):
    """Shopping cart model"""
    __tablename__ = "carts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="carts")
    items: Mapped[List["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Cart(id={self.id}, user_id={self.user_id})>"
    
    @property
    def total_amount(self) -> float:
        """Calculate total amount of items in cart"""
        return sum(item.subtotal for item in self.items)
    
    @property
    def total_items(self) -> int:
        """Calculate total number of items in cart"""
        return sum(item.quantity for item in self.items)

class CartItem(Base):
    """Cart item model"""
    __tablename__ = "cart_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    cart: Mapped[Cart] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
    
    def __repr__(self) -> str:
        return f"<CartItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
    
    @property
    def subtotal(self) -> float:
        """Calculate subtotal for this cart item"""
        return float(self.product.price) * self.quantity