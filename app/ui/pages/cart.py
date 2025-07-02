"""Shopping cart page"""
from nicegui import ui
from app.ui.state import AppState

class CartPage:
    """Shopping cart page component"""
    
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self._create_page()
    
    def _create_page(self):
        """Create the cart page"""
        with ui.column().classes('w-full max-w-4xl mx-auto px-4 py-8 gap-8'):
            # Page header
            ui.label('Shopping Cart').classes('text-3xl font-bold')
            
            # Cart contents
            self._create_cart_contents()
    
    def _create_cart_contents(self):
        """Create cart contents"""
        cart = self.app_state.get_cart()
        
        if not cart or not cart.items:
            self._create_empty_cart()
            return
        
        # Cart items
        with ui.column().classes('w-full gap-4'):
            for item in cart.items:
                self._create_cart_item(item)
        
        # Cart summary
        self._create_cart_summary(cart)
    
    def _create_empty_cart(self):
        """Create empty cart message"""
        with ui.column().classes('w-full text-center py-12'):
            ui.icon('shopping_cart', size='4rem').classes('text-gray-400 mb-4')
            ui.label('Your cart is empty').classes('text-xl text-gray-500 mb-2')
            ui.label('Add some products to get started').classes('text-gray-400 mb-6')
            ui.button(
                'Continue Shopping',
                icon='shopping_bag',
                on_click=lambda: ui.navigate.to('/products')
            ).classes('apple-button')
    
    def _create_cart_item(self, item):
        """Create cart item row"""
        with ui.card().classes('w-full p-4'):
            with ui.row().classes('w-full items-center gap-4'):
                # Product image placeholder
                ui.image('/static/images/apple-logo.png').classes('w-16 h-16 object-cover rounded')
                
                # Product details
                with ui.column().classes('flex-1'):
                    ui.label(item.product.name).classes('font-semibold text-lg')
                    ui.label(f'${item.product.price:,.2f}').classes('text-blue-600 font-medium')
                
                # Quantity controls
                with ui.row().classes('items-center gap-2'):
                    ui.button(
                        icon='remove',
                        on_click=lambda item_id=item.product_id: self._decrease_quantity(item_id, item.quantity)
                    ).classes('w-8 h-8 rounded-full')
                    
                    ui.label(str(item.quantity)).classes('w-8 text-center font-medium')
                    
                    ui.button(
                        icon='add',
                        on_click=lambda item_id=item.product_id: self._increase_quantity(item_id, item.quantity)
                    ).classes('w-8 h-8 rounded-full')
                
                # Subtotal
                ui.label(f'${item.subtotal:,.2f}').classes('font-semibold text-lg w-20 text-right')
                
                # Remove button
                ui.button(
                    icon='delete',
                    on_click=lambda item_id=item.product_id: self._remove_item(item_id)
                ).classes('text-red-500 hover:bg-red-50')
    
    def _create_cart_summary(self, cart):
        """Create cart summary"""
        with ui.card().classes('w-full p-6 mt-6'):
            with ui.column().classes('gap-4'):
                ui.label('Order Summary').classes('text-xl font-semibold mb-4')
                
                with ui.row().classes('w-full justify-between'):
                    ui.label(f'Total Items: {cart.total_items}').classes('text-gray-600')
                    ui.label(f'${cart.total_amount:,.2f}').classes('text-2xl font-bold text-blue-600')
                
                ui.separator()
                
                with ui.row().classes('w-full gap-4'):
                    ui.button(
                        'Continue Shopping',
                        icon='shopping_bag',
                        on_click=lambda: ui.navigate.to('/products')
                    ).classes('flex-1 bg-gray-200 text-gray-800 hover:bg-gray-300')
                    
                    ui.button(
                        'Proceed to Checkout',
                        icon='payment',
                        on_click=lambda: ui.navigate.to('/checkout')
                    ).classes('flex-1 apple-button')
    
    def _increase_quantity(self, product_id: int, current_quantity: int):
        """Increase item quantity"""
        if self.app_state.update_cart_item(product_id, current_quantity + 1):
            ui.navigate.to('/cart')  # Refresh page
        else:
            ui.notify('Failed to update quantity', type='negative')
    
    def _decrease_quantity(self, product_id: int, current_quantity: int):
        """Decrease item quantity"""
        if current_quantity > 1:
            if self.app_state.update_cart_item(product_id, current_quantity - 1):
                ui.navigate.to('/cart')  # Refresh page
            else:
                ui.notify('Failed to update quantity', type='negative')
        else:
            self._remove_item(product_id)
    
    def _remove_item(self, product_id: int):
        """Remove item from cart"""
        if self.app_state.remove_from_cart(product_id):
            ui.notify('Item removed from cart', type='positive')
            ui.navigate.to('/cart')  # Refresh page
        else:
            ui.notify('Failed to remove item', type='negative')