"""UI components package"""

try:
    from app.ui.components.navigation import Navigation
    from app.ui.components.product_card import ProductCard
    
    __all__ = ["Navigation", "ProductCard"]
    
except ImportError as e:
    import logging
    logging.error(f"Failed to import UI components: {e}")
    __all__ = []