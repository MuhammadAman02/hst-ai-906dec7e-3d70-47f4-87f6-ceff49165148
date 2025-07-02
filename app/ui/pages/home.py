"""Home page"""
from nicegui import ui
from app.ui.state import AppState
from app.ui.components.product_card import ProductCard

class HomePage:
    """Home page component"""
    
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self._create_page()
    
    def _create_page(self):
        """Create the home page"""
        with ui.column().classes('w-full max-w-7xl mx-auto px-4 py-8 gap-12'):
            # Hero section
            self._create_hero_section()
            
            # Featured products
            self._create_featured_section()
            
            # Categories
            self._create_categories_section()
    
    def _create_hero_section(self):
        """Create hero section"""
        with ui.card().classes('apple-gradient w-full p-12 text-center text-white'):
            ui.label('Welcome to Apple Store').classes('text-4xl font-bold mb-4')
            ui.label('Discover the latest Apple products and innovations').classes('text-xl mb-8')
            ui.button(
                'Shop Now',
                icon='shopping_bag',
                on_click=lambda: ui.navigate.to('/products')
            ).classes('apple-button text-lg px-8 py-3')
    
    def _create_featured_section(self):
        """Create featured products section"""
        ui.label('Featured Products').classes('text-3xl font-bold text-center mb-8')
        
        featured_products = self.app_state.get_featured_products()
        
        if featured_products:
            with ui.grid(columns=4).classes('w-full gap-6'):
                for product in featured_products[:8]:  # Show max 8 products
                    ProductCard(product, self.app_state)
        else:
            ui.label('No featured products available').classes('text-center text-gray-500')
    
    def _create_categories_section(self):
        """Create categories section"""
        ui.label('Shop by Category').classes('text-3xl font-bold text-center mb-8')
        
        categories = self.app_state.get_categories()
        
        if categories:
            with ui.grid(columns=3).classes('w-full gap-6'):
                for category in categories:
                    with ui.card().classes('apple-card p-6 text-center cursor-pointer hover:shadow-lg transition-shadow'):
                        ui.icon('category', size='3rem').classes('text-blue-600 mb-4')
                        ui.label(category.name).classes('text-xl font-semibold mb-2')
                        if category.description:
                            ui.label(category.description).classes('text-gray-600 mb-4')
                        ui.button(
                            'Browse',
                            on_click=lambda cat_id=category.id: self._browse_category(cat_id)
                        ).classes('apple-button')
        else:
            ui.label('No categories available').classes('text-center text-gray-500')
    
    def _browse_category(self, category_id: int):
        """Navigate to products page with category filter"""
        self.app_state.selected_category = category_id
        self.app_state.search_query = ""
        ui.navigate.to('/products')