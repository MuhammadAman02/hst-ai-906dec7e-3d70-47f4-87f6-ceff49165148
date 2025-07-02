"""Order service for order processing"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app.core.exceptions import CartEmptyError, InsufficientStockError
from app.services.cart_service import CartService

class OrderService:
    """Service for order-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.cart_service = CartService(db)
    
    def create_order_from_cart(self, user_id: int) -> Order:
        """Create order from user's cart"""
        cart = self.cart_service.get_cart_contents(user_id)
        
        if not cart.items:
            raise CartEmptyError()
        
        # Verify stock availability for all items
        for cart_item in cart.items:
            product = cart_item.product
            if not product.can_fulfill_quantity(cart_item.quantity):
                raise InsufficientStockError(
                    product.name, 
                    cart_item.quantity, 
                    product.stock
                )
        
        # Create order
        order = Order(
            user_id=user_id,
            total=cart.total_amount,
            status="pending"
        )
        self.db.add(order)
        self.db.flush()  # Get order ID
        
        # Create order items and update stock
        for cart_item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            self.db.add(order_item)
            
            # Update product stock
            product = cart_item.product
            product.stock -= cart_item.quantity
        
        # Clear cart
        self.cart_service.clear_cart(user_id)
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_user_orders(self, user_id: int) -> List[Order]:
        """Get all orders for a user"""
        query = select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
        return list(self.db.execute(query).scalars().all())
    
    def get_order(self, order_id: int) -> Order:
        """Get order by ID"""
        return self.db.get(Order, order_id)
    
    def update_order_status(self, order_id: int, status: str) -> Order:
        """Update order status"""
        order = self.get_order(order_id)
        if order:
            order.status = status
            self.db.commit()
            self.db.refresh(order)
        return order