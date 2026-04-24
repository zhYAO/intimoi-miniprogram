"""Tests for cart service."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.member import Member
from app.models.cart import Cart
from app.models.goods import Goods
from app.models.goods_spec import GoodsSpec


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_cart_add_and_get(db_session):
    """Test adding item to cart and retrieving it."""
    # Create member
    member = Member(open_id="test_open_id_123", level=1)
    db_session.add(member)
    db_session.flush()
    
    # Create goods and spec
    goods = Goods(goods_id="G001", goods_name="Test Goods", price=100)
    db_session.add(goods)
    spec = GoodsSpec(spec_id="S001", goods_id="G001", spec_name="30ml", price=100, stock=10)
    db_session.add(spec)
    db_session.flush()
    
    # Add to cart
    cart_item = Cart(member_id=member.id, goods_id="G001", spec_id="S001", num=2)
    db_session.add(cart_item)
    db_session.commit()
    
    # Verify
    items = db_session.query(Cart).filter(Cart.member_id == member.id).all()
    assert len(items) == 1
    assert items[0].num == 2
    assert items[0].goods_id == "G001"


def test_cart_update_quantity(db_session):
    """Test updating cart item quantity."""
    member = Member(open_id="test_open_id_456", level=1)
    db_session.add(member)
    db_session.flush()
    
    cart_item = Cart(member_id=member.id, goods_id="G001", spec_id="S001", num=1)
    db_session.add(cart_item)
    db_session.commit()
    
    # Update quantity
    cart_item.num = 5
    db_session.commit()
    
    updated = db_session.query(Cart).filter(Cart.id == cart_item.id).first()
    assert updated.num == 5


def test_cart_delete(db_session):
    """Test deleting cart item."""
    member = Member(open_id="test_open_id_789", level=1)
    db_session.add(member)
    db_session.flush()
    
    cart_item = Cart(member_id=member.id, goods_id="G001", spec_id="S001", num=1)
    db_session.add(cart_item)
    db_session.commit()
    
    db_session.delete(cart_item)
    db_session.commit()
    
    remaining = db_session.query(Cart).filter(Cart.member_id == member.id).all()
    assert len(remaining) == 0


def test_cart_select_all(db_session):
    """Test select all / deselect all."""
    member = Member(open_id="test_select_all", level=1)
    db_session.add(member)
    db_session.flush()
    
    for i in range(3):
        item = Cart(member_id=member.id, goods_id=f"G00{i}", spec_id=f"S00{i}", num=1, selected=1)
        db_session.add(item)
    db_session.commit()
    
    # Deselect all
    db_session.query(Cart).filter(Cart.member_id == member.id).update({"selected": 0})
    db_session.commit()
    
    items = db_session.query(Cart).filter(Cart.member_id == member.id).all()
    assert all(item.selected == 0 for item in items)
