# Apple Online Store

A modern e-commerce platform built with NiceGUI and FastAPI, featuring a sleek Apple-inspired design.

## Features

- 🛍️ **Product Catalog**: Browse Apple products by category
- 🛒 **Shopping Cart**: Add, remove, and manage cart items
- 💳 **Checkout Process**: Complete order processing
- 🔍 **Search Functionality**: Find products quickly
- 📱 **Responsive Design**: Apple-inspired modern UI
- 🗄️ **Database Integration**: SQLAlchemy with SQLite

## Quick Start

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd apple-online-store
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

3. **Access the Store**:
   Open your browser to `http://localhost:8080`

## Demo Account

- **Email**: demo@apple.com
- **Password**: demo123

## Project Structure

```
apple-online-store/
├── app/
│   ├── core/           # Core configuration and database
│   ├── models/         # SQLAlchemy models
│   ├── services/       # Business logic layer
│   ├── ui/            # NiceGUI frontend
│   │   ├── components/ # Reusable UI components
│   │   └── pages/     # Page components
│   └── static/        # Static assets
├── data/              # Database files
└── main.py           # Application entry point
```

## Technology Stack

- **Frontend**: NiceGUI (Python-based web UI)
- **Backend**: FastAPI with SQLAlchemy
- **Database**: SQLite (development), PostgreSQL ready
- **Authentication**: Passlib with bcrypt
- **Styling**: Tailwind CSS classes

## Key Features

### Product Management
- Category-based product organization
- Product search and filtering
- Stock management
- Featured products display

### Shopping Cart
- Session-based cart management
- Quantity updates
- Real-time total calculations
- Persistent cart storage

### Order Processing
- Complete checkout workflow
- Order history tracking
- Stock deduction on purchase
- Order status management

### User Interface
- Apple-inspired design language
- Responsive grid layouts
- Interactive product cards
- Smooth navigation

## Development

### Adding New Products
Products are initialized in `app/core/database.py` in the `init_sample_data()` function.

### Customizing UI
UI components are in `app/ui/components/` and pages in `app/ui/pages/`.

### Database Schema
Models are defined in `app/models/` using SQLAlchemy V2 patterns.

## Production Deployment

1. **Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Database Migration**:
   ```bash
   # For PostgreSQL in production
   pip install psycopg2-binary
   # Update DATABASE_URL in .env
   ```

3. **Security**:
   - Change SECRET_KEY in production
   - Use HTTPS
   - Configure proper CORS settings
   - Set DEBUG=false

## API Endpoints

The application includes a REST API layer:

- `GET /api/products` - List products
- `GET /api/categories` - List categories
- `POST /api/cart/add` - Add to cart
- `GET /api/cart` - Get cart contents
- `POST /api/orders` - Create order

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.