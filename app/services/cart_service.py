"""Cart service for shopping cart operations"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.core.exceptions import ProductNotFoundError, InsufficientStockError

class CartService:
    """Service for cart-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_cart(self, user_id: int) -> Cart:
        """Get existing cart or create new one for user"""
        # Try to get existing cart
        query = select(Cart).where(Cart.user_id == user_id)
        cart = self.db.execute(query).scalar_one_or_none()
        
        if not cart:
            cart = Cart(user_id=user_id)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        
        return cart
    
    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
        """Add product to cart"""
        # Verify product exists and has sufficient stock
        product = self.db.get(Product, product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        
        if not product.can_fulfill_quantity(quantity):
            raise InsufficientStockError(product.name, quantity, product.stock)
        
        # Get or create cart
        cart = self.get_or_create_cart(user_id)
        
        # Check if item already exists in cart
        query = select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
        existing_item = self.db.execute(query).scalar_one_or_none()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            if not product.can_fulfill_quantity(new_quantity):
                raise InsufficientStockError(product.name, new_quantity, product.stock)
            
            existing_item.quantity = new_quantity
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            self.db.add(cart_item)
        
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item
    
    def update_cart_item(self, user_id: int, product_id: int, quantity: int) -> Optional[CartItem]:
        """Update cart item quantity"""
        cart = self.get_or_create_cart(user_id)
        
        query = select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
        cart_item = self.db.execute(query).scalar_one_or_none()
        
        if not cart_item:
            return None
        
        if quantity <= 0:
            # Remove item from cart
            self.db.delete(cart_item)
            self.db.commit()
            return None
        
        # Verify stock availability
        product = self.db.get(Product, product_id)
        if not product.can_fulfill_quantity(quantity):
            raise InsufficientStockError(product.name, quantity, product.stock)
        
        cart_item.quantity = quantity
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item
    
    def remove_from_cart(self, user_id: int, product_id: int) -> bool:
        """Remove product from cart"""
        cart = self.get_or_create_cart(user_id)
        
        query = select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
        cart_item = self.db.execute(query).scalar_one_or_none()
        
        if cart_item:
            self.db.delete(cart_item)
            self.db.commit()
            return True
        
        return False
    
    def get_cart_contents(self, user_id: int) -> Cart:
        """Get cart with all items"""
        cart = self.get_or_create_cart(user_id)
        # Refresh to get latest items
        self.db.refresh(cart)
        return cart
    
    def clear_cart(self, user_id: int) -> bool:
        """Clear all items from cart"""
        cart = self.get_or_create_cart(user_id)
        
        for item in cart.items:
            self.db.delete(item)
        
        self.db.commit()
        return True