"""Product and Category models"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Numeric, ForeignKey, DateTime, func
from datetime import datetime
from typing import List, Optional
from app.core.database import Base

class Category(Base):
    """Product category model"""
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    products: Mapped[List["Product"]] = relationship(back_populates="category")
    
    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"

class Product(Base):
    """Product model"""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    category: Mapped[Category] = relationship(back_populates="products")
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
    
    @property
    def is_in_stock(self) -> bool:
        """Check if product is in stock"""
        return self.stock > 0
    
    def can_fulfill_quantity(self, quantity: int) -> bool:
        """Check if we can fulfill the requested quantity"""
        return self.stock >= quantity