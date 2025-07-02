"""Custom exception classes for the application"""

class AppError(Exception):
    """Base exception class for application errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ProductNotFoundError(AppError):
    """Raised when a product is not found"""
    def __init__(self, product_id: int):
        message = f"Product with ID {product_id} not found"
        super().__init__(message, status_code=404)

class CategoryNotFoundError(AppError):
    """Raised when a category is not found"""
    def __init__(self, category_id: int):
        message = f"Category with ID {category_id} not found"
        super().__init__(message, status_code=404)

class InsufficientStockError(AppError):
    """Raised when there's insufficient stock for a product"""
    def __init__(self, product_name: str, requested: int, available: int):
        message = f"Insufficient stock for {product_name}. Requested: {requested}, Available: {available}"
        super().__init__(message, status_code=400)

class CartEmptyError(AppError):
    """Raised when trying to checkout with an empty cart"""
    def __init__(self):
        message = "Cannot checkout with an empty cart"
        super().__init__(message, status_code=400)

class UserNotFoundError(AppError):
    """Raised when a user is not found"""
    def __init__(self, user_id: int):
        message = f"User with ID {user_id} not found"
        super().__init__(message, status_code=404)

__all__ = [
    "AppError",
    "ProductNotFoundError", 
    "CategoryNotFoundError",
    "InsufficientStockError",
    "CartEmptyError",
    "UserNotFoundError"
]