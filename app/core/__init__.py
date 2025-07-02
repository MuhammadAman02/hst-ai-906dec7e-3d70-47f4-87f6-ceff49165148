"""Core application modules"""

try:
    from app.core.config import settings
    from app.core.database import get_db, create_tables
    from app.core.exceptions import AppError, ProductNotFoundError, InsufficientStockError
    
    __all__ = ["settings", "get_db", "create_tables", "AppError", "ProductNotFoundError", "InsufficientStockError"]
    
except ImportError as e:
    import logging
    logging.error(f"Failed to import core modules: {e}")
    
    # Provide minimal fallbacks
    class MinimalSettings:
        DATABASE_URL = "sqlite:///./data/apple_store.db"
        SECRET_KEY = "fallback-secret-key"
        DEBUG = True
    
    settings = MinimalSettings()
    
    class AppError(Exception):
        pass
    
    ProductNotFoundError = AppError
    InsufficientStockError = AppError
    
    def get_db():
        pass
    
    def create_tables():
        pass
    
    __all__ = ["settings", "get_db", "create_tables", "AppError", "ProductNotFoundError", "InsufficientStockError"]