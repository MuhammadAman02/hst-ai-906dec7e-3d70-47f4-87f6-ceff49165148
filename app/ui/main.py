"""Main NiceGUI application"""
from nicegui import ui, app
from app.ui.pages.home import HomePage
from app.ui.pages.products import ProductsPage
from app.ui.pages.cart import CartPage
from app.ui.pages.checkout import CheckoutPage
from app.ui.components.navigation import Navigation
from app.ui.state import AppState
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the NiceGUI application"""
    
    # Initialize application state
    app_state = AppState()
    
    # Configure NiceGUI
    ui.run_with.uvicorn_config(
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
    
    # Add custom CSS for Apple-like styling
    ui.add_head_html('''
    <style>
        .apple-gradient {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .apple-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .apple-button {
            background: #007AFF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .apple-button:hover {
            background: #0056CC;
            transform: translateY(-1px);
        }
        .product-card {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .product-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
    </style>
    ''')
    
    # Setup routes
    @ui.page('/')
    def home_page():
        with ui.column().classes('w-full min-h-screen bg-gray-50'):
            Navigation(app_state)
            HomePage(app_state)
    
    @ui.page('/products')
    def products_page():
        with ui.column().classes('w-full min-h-screen bg-gray-50'):
            Navigation(app_state)
            ProductsPage(app_state)
    
    @ui.page('/cart')
    def cart_page():
        with ui.column().classes('w-full min-h-screen bg-gray-50'):
            Navigation(app_state)
            CartPage(app_state)
    
    @ui.page('/checkout')
    def checkout_page():
        with ui.column().classes('w-full min-h-screen bg-gray-50'):
            Navigation(app_state)
            CheckoutPage(app_state)
    
    logger.info(f"Apple Store application created successfully")
    return app