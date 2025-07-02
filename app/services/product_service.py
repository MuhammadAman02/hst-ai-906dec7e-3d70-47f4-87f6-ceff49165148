"""Product service for business logic"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models.product import Product, Category
from app.core.exceptions import ProductNotFoundError, CategoryNotFoundError

class ProductService:
    """Service for product-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_products(self, category_id: Optional[int] = None) -> List[Product]:
        """Get all products, optionally filtered by category"""
        query = select(Product)
        if category_id:
            query = query.where(Product.category_id == category_id)
        return list(self.db.execute(query).scalars().all())
    
    def get_product(self, product_id: int) -> Product:
        """Get product by ID"""
        product = self.db.get(Product, product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product
    
    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        return list(self.db.execute(select(Category)).scalars().all())
    
    def get_category(self, category_id: int) -> Category:
        """Get category by ID"""
        category = self.db.get(Category, category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        return category
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or description"""
        search_query = select(Product).where(
            Product.name.ilike(f"%{query}%") |
            Product.description.ilike(f"%{query}%")
        )
        return list(self.db.execute(search_query).scalars().all())
    
    def get_featured_products(self, limit: int = 8) -> List[Product]:
        """Get featured products (highest priced items)"""
        query = select(Product).order_by(Product.price.desc()).limit(limit)
        return list(self.db.execute(query).scalars().all())