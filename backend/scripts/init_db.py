"""Database initialization script."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, init_db
from app.models import Base
from app.models.member import Member
from app.models.member_address import MemberAddress
from app.models.cart import Cart
from app.models.goods import Goods
from app.models.goods_spec import GoodsSpec
from app.models.favorites import Favorites
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.wdt_config import WdtConfig
from app.models.category import Category


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    init_db()
    print("Tables created successfully!")


def insert_sample_data():
    """Insert sample data for testing."""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Member).count() > 0:
            print("Sample data already exists, skipping...")
            return
        
        # Insert sample WDT config
        wdt_config = WdtConfig(
            env="test",
            appkey="appkey_market_test",
            appsecret="***",  # encrypted placeholder
            sid="haijun",
            base_url="https://openapitest.huice.com/openapi/",
            is_active=1,
        )
        db.add(wdt_config)
        
        # Insert sample goods
        goods1 = Goods(
            goods_id="18344",
            goods_name="精粹修护精华液",
            goods_no="GH001",
            category_id=1,
            price=1280.00,
            original_price=1680.00,
            description="<p>富含高浓度精粹成分，专注修护肌肤屏障。</p>",
            images='["https://example.com/goods/18344/img1.jpg","https://example.com/goods/18344/img2.jpg"]',
            sales=328,
            is_on_sale=1,
        )
        db.add(goods1)
        db.flush()
        
        # Insert specs
        spec1 = GoodsSpec(
            spec_id="18656",
            goods_id="18344",
            spec_no="GHSKU001",
            spec_name="30ml",
            price=1280.00,
            stock=99,
            is_on_sale=1,
        )
        spec2 = GoodsSpec(
            spec_id="18657",
            goods_id="18344",
            spec_no="GHSKU002",
            spec_name="50ml",
            price=1980.00,
            stock=50,
            is_on_sale=1,
        )
        db.add_all([spec1, spec2])
        
        # Insert categories
        cat1 = Category(name="精华液", sort=1, is_active=1)
        cat2 = Category(name="面霜", sort=2, is_active=1)
        db.add_all([cat1, cat2])
        
        db.commit()
        print("Sample data inserted successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error inserting sample data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-sample-data", action="store_true", help="Insert sample data after creating tables")
    args = parser.parse_args()
    
    create_tables()
    if args.with_sample_data:
        insert_sample_data()
