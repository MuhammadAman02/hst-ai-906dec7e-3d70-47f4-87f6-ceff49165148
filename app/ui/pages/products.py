"""Products page"""
from nicegui import ui
from app.ui.state import AppState
from app.ui.components.product_card import ProductCard

class ProductsPage:
    """Products page component"""
    
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self._create_page()
    
    def _create_page(self):
        """Create the products page"""
        with ui.column().classes('w-full max-w-7xl mx-auto px-4 py-8 gap-8'):
            # Page header
            self._create_header()
            
            # Filters and search
            self._create_filters()
            
            # Products grid
            self._create_products_grid()
    
    def _create_header(self):
        """Create page header"""
        if self.app_state.search_query:
            ui.label(f'Search Results for "{self.app_state.search_query}"').classes('text-3xl font-bold')
        elif self.app_state.selected_category:
            categories = self.app_state.get_categories()
            category_name = next((cat.name for cat in categories if cat.id == self.app_state.selected_category), "Products")
            ui.label(category_name).classes('text-3xl font-bold')
        else:
            ui.label('All Products').classes('text-3xl font-bold')
    
    def _create_filters(self):
        """Create filters section"""
        with ui.row().classes('w-full items-center gap-4 mb-6'):
            # Category filter
            categories = self.app_state.get_categories()
            category_options = [{'label': 'All Categories', 'value': None}]
            category_options.extend([{'label': cat.name, 'value': cat.id} for cat in categories])
            
            category_select = ui.select(
                options=category_options,
                value=self.app_state.selected_category,
                label='Category'
            ).classes('w-48')
            category_select.on('update:model-value', lambda e: self._filter_by_category(e.args))
            
            # Clear filters button
            ui.button(
                'Clear Filters',
                icon='clear',
                on_click=self._clear_filters
            ).classes('apple-button')
    
    def _create_products_grid(self):
        """Create products grid"""
        products = self.app_state.get_products(self.app_state.selected_category)
        
        if products:
            with ui.grid(columns=4).classes('w-full gap-6'):
                for product in products:
                    ProductCard(product, self.app_state)
        else:
            with ui.column().classes('w-full text-center py-12'):
                ui.icon('inventory_2', size='4rem').classes('text-gray-400 mb-4')
                ui.label('No products found').classes('text-xl text-gray-500 mb-2')
                ui.label('Try adjusting your search or filters').classes('text-gray-400')
    
    def _filter_by_category(self, category_id):
        """Filter products by category"""
        self.app_state.selected_category = category_id
        self.app_state.search_query = ""
        ui.navigate.to('/products')  # Refresh page
    
    def _clear_filters(self):
        """Clear all filters"""
        self.app_state.selected_category = None
        self.app_state.search_query = ""
        ui.navigate.to('/products')  # Refresh page