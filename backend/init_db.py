from app.database import engine, Base
from app.models import User, ShopifyStore, Product, Order

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
