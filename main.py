"""Apple Online Store - Main Application Entry Point"""
import os
import sys
import logging
from pathlib import Path

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create required directories
for directory in ["data", "app/static/images", "logs"]:
    Path(directory).mkdir(parents=True, exist_ok=True)

try:
    from app.core.database import create_tables, init_sample_data
    from app.ui.main import create_app
    from app.core.config import settings
    
    # Initialize database
    create_tables()
    init_sample_data()
    
    # Create and run the application
    app = create_app()
    
except Exception as e:
    logging.error(f"Failed to start application: {e}")
    sys.exit(1)