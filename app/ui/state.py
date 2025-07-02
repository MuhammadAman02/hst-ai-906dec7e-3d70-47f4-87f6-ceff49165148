"""Application state management"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.services.user_service import UserService
from app.models.user import User
from app.models.product import Product, Category
from app.models.cart import Cart
import logging

logger = logging.getLogger(__name__)

class AppState:
    """Global application state management"""
    
    def __init__(self):
        self.current_user: Optional[User] = None
        self.selected_category: Optional[int] = None
        self.search_query: str = ""
        self.cart_items_count: int = 0
        
        # Initialize with demo user for simplicity
        self._initialize_demo_user()
    
    def _initialize_demo_user(self):
        """Initialize with demo user for demonstration"""
        try:
            db = next(get_db())
            user_service = UserService(db)
            self.current_user = user_service.get_user_by_email("demo@apple.com")
            if self.current_user:
                self._update_cart_count()
                logger.info(f"Initialized with demo user: {self.current_user.email}")
        except Exception as e:
            logger.error(f"Failed to initialize demo user: {e}")
    
    def _update_cart_count(self):
        """Update cart items count"""
        if not self.current_user:
            self.cart_items_count = 0
            return
        
        try:
            db = next(get_db())
            cart_service = CartService(db)
            cart = cart_service.get_cart_contents(self.current_user.id)
            self.cart_items_count = cart.total_items
        except Exception as e:
            logger.error(f"Failed to update cart count: {e}")
            self.cart_items_count = 0
    
    def get_products(self, category_id: Optional[int] = None) -> List[Product]:
        """Get products, optionally filtered by category"""
        try:
            db = next(get_db())
            product_service = ProductService(db)
            
            if self.search_query:
                return product_service.search_products(self.search_query)
            else:
                return product_service.get_all_products(category_id)
        except Exception as e:
            logger.error(f"Failed to get products: {e}")
            return []
    
    def get_categories(self) -> List[Category]:
        """Get all categories"""
        try:
            db = next(get_db())
            product_service = ProductService(db)
            return product_service.get_all_categories()
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            return []
    
    def get_featured_products(self) -> List[Product]:
        """Get featured products"""
        try:
            db = next(get_db())
            product_service = ProductService(db)
            return product_service.get_featured_products()
        except Exception as e:
            logger.error(f"Failed to get featured products: {e}")
            return []
    
    def add_to_cart(self, product_id: int, quantity: int = 1) -> bool:
        """Add product to cart"""
        if not self.current_user:
            return False
        
        try:
            db = next(get_db())
            cart_service = CartService(db)
            cart_service.add_to_cart(self.current_user.id, product_id, quantity)
            self._update_cart_count()
            return True
        except Exception as e:
            logger.error(f"Failed to add to cart: {e}")
            return False
    
    def get_cart(self) -> Optional[Cart]:
        """Get current user's cart"""
        if not self.current_user:
            return None
        
        try:
            db = next(get_db())
            cart_service = CartService(db)
            return cart_service.get_cart_contents(self.current_user.id)
        except Exception as e:
            logger.error(f"Failed to get cart: {e}")
            return None
    
    def update_cart_item(self, product_id: int, quantity: int) -> bool:
        """Update cart item quantity"""
        if not self.current_user:
            return False
        
        try:
            db = next(get_db())
            cart_service = CartService(db)
            cart_service.update_cart_item(self.current_user.id, product_id, quantity)
            self._update_cart_count()
            return True
        except Exception as e:
            logger.error(f"Failed to update cart item: {e}")
            return False
    
    def remove_from_cart(self, product_id: int) -> bool:
        """Remove product from cart"""
        if not self.current_user:
            return False
        
        try:
            db = next(get_db())
            cart_service = CartService(db)
            cart_service.remove_from_cart(self.current_user.id, product_id)
            self._update_cart_count()
            return True
        except Exception as e:
            logger.error(f"Failed to remove from cart: {e}")
            return False
    
    def checkout(self) -> bool:
        """Process checkout"""
        if not self.current_user:
            return False
        
        try:
            db = next(get_db())
            order_service = OrderService(db)
            order = order_service.create_order_from_cart(self.current_user.id)
            self._update_cart_count()
            logger.info(f"Order created successfully: {order.id}")
            return True
        except Exception as e:
            logger.error(f"Failed to process checkout: {e}")
            return False