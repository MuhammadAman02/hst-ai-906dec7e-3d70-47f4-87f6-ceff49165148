"""UI pages package"""

try:
    from app.ui.pages.home import HomePage
    from app.ui.pages.products import ProductsPage
    from app.ui.pages.cart import CartPage
    from app.ui.pages.checkout import CheckoutPage
    
    __all__ = ["HomePage", "ProductsPage", "CartPage", "CheckoutPage"]
    
except ImportError as e:
    import logging
    logging.error(f"Failed to import UI pages: {e}")
    __all__ = []