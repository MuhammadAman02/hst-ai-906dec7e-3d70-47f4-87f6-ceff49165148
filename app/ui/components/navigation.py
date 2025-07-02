"""Navigation component"""
from nicegui import ui
from app.ui.state import AppState

class Navigation:
    """Main navigation component"""
    
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self._create_navigation()
    
    def _create_navigation(self):
        """Create the navigation bar"""
        with ui.header().classes('bg-white shadow-sm border-b'):
            with ui.row().classes('w-full max-w-7xl mx-auto px-4 py-3 items-center justify-between'):
                # Logo and brand
                with ui.row().classes('items-center gap-4'):
                    ui.icon('apple', size='2rem').classes('text-gray-800')
                    ui.label('Apple Store').classes('text-2xl font-bold text-gray-800')
                
                # Navigation links
                with ui.row().classes('items-center gap-6'):
                    ui.link('Home', '/').classes('text-gray-600 hover:text-gray-800 font-medium')
                    ui.link('Products', '/products').classes('text-gray-600 hover:text-gray-800 font-medium')
                    
                    # Search bar
                    search_input = ui.input(placeholder='Search products...').classes('w-64')
                    search_input.on('keydown.enter', lambda: self._handle_search(search_input.value))
                    
                    # Cart button
                    with ui.button(icon='shopping_cart', on_click=lambda: ui.navigate.to('/cart')).classes('relative'):
                        if self.app_state.cart_items_count > 0:
                            ui.badge(str(self.app_state.cart_items_count)).classes('absolute -top-2 -right-2 bg-red-500 text-white')
                    
                    # User info
                    if self.app_state.current_user:
                        ui.label(f'Welcome, {self.app_state.current_user.username}').classes('text-sm text-gray-600')
    
    def _handle_search(self, query: str):
        """Handle search functionality"""
        self.app_state.search_query = query.strip()
        ui.navigate.to('/products')