"""UI package for NiceGUI frontend"""

try:
    from app.ui.main import create_app
    
    __all__ = ["create_app"]
    
except ImportError as e:
    import logging
    logging.error(f"Failed to import UI modules: {e}")
    
    def create_app():
        print("UI modules not available")
        return None
    
    __all__ = ["create_app"]