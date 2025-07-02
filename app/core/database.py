"""Database configuration and session management using SQLAlchemy V2"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.pool import StaticPool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create engine with proper SQLite configuration
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False,
        "timeout": 20
    }
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass

def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def get_db() -> Session:
    """Database session dependency"""
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

def init_sample_data():
    """Initialize the database with sample Apple products"""
    from app.models.product import Product, Category
    from app.models.user import User
    from app.core.security import get_password_hash
    
    with Session(engine) as session:
        # Check if data already exists
        if session.query(Category).first():
            logger.info("Sample data already exists, skipping initialization")
            return
        
        try:
            # Create categories
            categories = [
                Category(name="iPhone", description="Latest iPhone models"),
                Category(name="iPad", description="iPad tablets and accessories"),
                Category(name="Mac", description="MacBook and iMac computers"),
                Category(name="Apple Watch", description="Apple Watch series"),
                Category(name="AirPods", description="Wireless earphones"),
                Category(name="Accessories", description="Apple accessories")
            ]
            
            for category in categories:
                session.add(category)
            session.flush()  # Get IDs for categories
            
            # Create products
            products = [
                # iPhone
                Product(
                    name="iPhone 15 Pro",
                    description="The most advanced iPhone ever with titanium design and A17 Pro chip",
                    price=999.00,
                    image_url="/static/images/iphone15pro.jpg",
                    category_id=categories[0].id,
                    stock=50
                ),
                Product(
                    name="iPhone 15",
                    description="iPhone 15 with Dynamic Island and 48MP camera",
                    price=799.00,
                    image_url="/static/images/iphone15.jpg",
                    category_id=categories[0].id,
                    stock=75
                ),
                Product(
                    name="iPhone 14",
                    description="iPhone 14 with advanced camera system",
                    price=699.00,
                    image_url="/static/images/iphone14.jpg",
                    category_id=categories[0].id,
                    stock=100
                ),
                
                # iPad
                Product(
                    name="iPad Pro 12.9\"",
                    description="iPad Pro with M2 chip and Liquid Retina XDR display",
                    price=1099.00,
                    image_url="/static/images/ipadpro.jpg",
                    category_id=categories[1].id,
                    stock=30
                ),
                Product(
                    name="iPad Air",
                    description="iPad Air with M1 chip and 10.9-inch display",
                    price=599.00,
                    image_url="/static/images/ipadair.jpg",
                    category_id=categories[1].id,
                    stock=40
                ),
                
                # Mac
                Product(
                    name="MacBook Pro 16\"",
                    description="MacBook Pro with M3 Pro chip and 16-inch display",
                    price=2499.00,
                    image_url="/static/images/macbookpro16.jpg",
                    category_id=categories[2].id,
                    stock=20
                ),
                Product(
                    name="MacBook Air 15\"",
                    description="MacBook Air with M2 chip and 15-inch display",
                    price=1299.00,
                    image_url="/static/images/macbookair15.jpg",
                    category_id=categories[2].id,
                    stock=35
                ),
                Product(
                    name="iMac 24\"",
                    description="iMac with M3 chip and 24-inch 4.5K display",
                    price=1299.00,
                    image_url="/static/images/imac24.jpg",
                    category_id=categories[2].id,
                    stock=25
                ),
                
                # Apple Watch
                Product(
                    name="Apple Watch Series 9",
                    description="Apple Watch Series 9 with S9 chip and Double Tap",
                    price=399.00,
                    image_url="/static/images/watchseries9.jpg",
                    category_id=categories[3].id,
                    stock=60
                ),
                Product(
                    name="Apple Watch Ultra 2",
                    description="Apple Watch Ultra 2 for extreme sports and adventures",
                    price=799.00,
                    image_url="/static/images/watchultra2.jpg",
                    category_id=categories[3].id,
                    stock=25
                ),
                
                # AirPods
                Product(
                    name="AirPods Pro (2nd gen)",
                    description="AirPods Pro with Active Noise Cancellation",
                    price=249.00,
                    image_url="/static/images/airpodspro.jpg",
                    category_id=categories[4].id,
                    stock=80
                ),
                Product(
                    name="AirPods (3rd gen)",
                    description="AirPods with Spatial Audio and MagSafe case",
                    price=179.00,
                    image_url="/static/images/airpods3.jpg",
                    category_id=categories[4].id,
                    stock=100
                ),
                
                # Accessories
                Product(
                    name="MagSafe Charger",
                    description="Wireless charger for iPhone with MagSafe",
                    price=39.00,
                    image_url="/static/images/magsafe.jpg",
                    category_id=categories[5].id,
                    stock=150
                ),
                Product(
                    name="Magic Keyboard",
                    description="Magic Keyboard with Touch ID for Mac",
                    price=179.00,
                    image_url="/static/images/magickeyboard.jpg",
                    category_id=categories[5].id,
                    stock=75
                )
            ]
            
            for product in products:
                session.add(product)
            
            # Create a demo user
            demo_user = User(
                email="demo@apple.com",
                username="demo",
                hashed_password=get_password_hash("demo123"),
                is_active=True
            )
            session.add(demo_user)
            
            session.commit()
            logger.info("Sample data initialized successfully")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error initializing sample data: {e}")
            raise