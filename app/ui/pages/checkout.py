"""Checkout page"""
from nicegui import ui
from app.ui.state import AppState

class CheckoutPage:
    """Checkout page component"""
    
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self._create_page()
    
    def _create_page(self):
        """Create the checkout page"""
        cart = self.app_state.get_cart()
        
        if not cart or not cart.items:
            self._create_empty_cart_message()
            return
        
        with ui.column().classes('w-full max-w-4xl mx-auto px-4 py-8 gap-8'):
            # Page header
            ui.label('Checkout').classes('text-3xl font-bold')
            
            with ui.row().classes('w-full gap-8'):
                # Order summary
                self._create_order_summary(cart)
                
                # Checkout form
                self._create_checkout_form(cart)
    
    def _create_empty_cart_message(self):
        """Create empty cart message"""
        with ui.column().classes('w-full max-w-4xl mx-auto px-4 py-8 text-center'):
            ui.label('Your cart is empty').classes('text-2xl text-gray-500 mb-4')
            ui.button(
                'Continue Shopping',
                icon='shopping_bag',
                on_click=lambda: ui.navigate.to('/products')
            ).classes('apple-button')
    
    def _create_order_summary(self, cart):
        """Create order summary section"""
        with ui.column().classes('flex-1'):
            with ui.card().classes('w-full p-6'):
                ui.label('Order Summary').classes('text-xl font-semibold mb-4')
                
                # Order items
                for item in cart.items:
                    with ui.row().classes('w-full justify-between items-center py-2'):
                        with ui.column():
                            ui.label(item.product.name).classes('font-medium')
                            ui.label(f'Qty: {item.quantity}').classes('text-sm text-gray-600')
                        ui.label(f'${item.subtotal:,.2f}').classes('font-medium')
                
                ui.separator().classes('my-4')
                
                # Total
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('Total').classes('text-xl font-bold')
                    ui.label(f'${cart.total_amount:,.2f}').classes('text-xl font-bold text-blue-600')
    
    def _create_checkout_form(self, cart):
        """Create checkout form"""
        with ui.column().classes('flex-1'):
            with ui.card().classes('w-full p-6'):
                ui.label('Shipping Information').classes('text-xl font-semibold mb-4')
                
                # Shipping form
                with ui.column().classes('gap-4'):
                    ui.input('Full Name', placeholder='Enter your full name').classes('w-full')
                    ui.input('Email', placeholder='Enter your email').classes('w-full')
                    ui.input('Address', placeholder='Enter your address').classes('w-full')
                    ui.input('City', placeholder='Enter your city').classes('w-full')
                    
                    with ui.row().classes('w-full gap-4'):
                        ui.input('State', placeholder='State').classes('flex-1')
                        ui.input('ZIP Code', placeholder='ZIP').classes('flex-1')
                
                ui.separator().classes('my-6')
                
                ui.label('Payment Information').classes('text-xl font-semibold mb-4')
                
                # Payment form
                with ui.column().classes('gap-4'):
                    ui.input('Card Number', placeholder='1234 5678 9012 3456').classes('w-full')
                    
                    with ui.row().classes('w-full gap-4'):
                        ui.input('Expiry Date', placeholder='MM/YY').classes('flex-1')
                        ui.input('CVV', placeholder='123').classes('flex-1')
                    
                    ui.input('Cardholder Name', placeholder='Name on card').classes('w-full')
                
                # Place order button
                ui.button(
                    f'Place Order - ${cart.total_amount:,.2f}',
                    icon='payment',
                    on_click=self._place_order
                ).classes('apple-button w-full mt-6 text-lg py-3')
    
    def _place_order(self):
        """Process the order"""
        if self.app_state.checkout():
            ui.notify('Order placed successfully!', type='positive')
            # Redirect to a success page or home
            ui.navigate.to('/')
        else:
            ui.notify('Failed to place order. Please try again.', type='negative')