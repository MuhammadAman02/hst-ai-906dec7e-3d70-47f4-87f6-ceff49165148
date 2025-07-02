"""Product card component"""
from nicegui import ui
from app.models.product import Product
from app.ui.state import AppState

class ProductCard:
    """Product card component"""
    
    def __init__(self, product: Product, app_state: AppState):
        self.product = product
        self.app_state = app_state
        self._create_card()
    
    def _create_card(self):
        """Create the product card"""
        with ui.card().classes('product-card apple-card w-full max-w-sm mx-auto'):
            # Product image placeholder
            with ui.column().classes('w-full'):
                ui.image('/static/images/apple-logo.png').classes('w-full h-48 object-cover rounded-t-lg')
                
                with ui.column().classes('p-4 gap-3'):
                    # Product name
                    ui.label(self.product.name).classes('text-lg font-semibold text-gray-800')
                    
                    # Product description
                    if self.product.description:
                        ui.label(self.product.description).classes('text-sm text-gray-600 line-clamp-2')
                    
                    # Price and stock
                    with ui.row().classes('items-center justify-between'):
                        ui.label(f'${self.product.price:,.2f}').classes('text-xl font-bold text-blue-600')
                        
                        if self.product.stock > 0:
                            ui.label(f'{self.product.stock} in stock').classes('text-xs text-green-600')
                        else:
                            ui.label('Out of stock').classes('text-xs text-red-600')
                    
                    # Add to cart button
                    if self.product.stock > 0:
                        ui.button(
                            'Add to Cart',
                            icon='add_shopping_cart',
                            on_click=lambda: self._add_to_cart()
                        ).classes('apple-button w-full')
                    else:
                        ui.button('Out of Stock').classes('w-full bg-gray-400 cursor-not-allowed').props('disabled')
    
    def _add_to_cart(self):
        """Add product to cart"""
        if self.app_state.add_to_cart(self.product.id):
            ui.notify(f'{self.product.name} added to cart!', type='positive')
        else:
            ui.notify('Failed to add product to cart', type='negative')