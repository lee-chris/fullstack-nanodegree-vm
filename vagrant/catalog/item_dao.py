import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from database_setup import Base, Category, Item


class ItemDao(object):
    
    def __init__(self):
        """Initialize ItemDao.
        
        This object will be initialized to read/write Items to an sqlite database
        saved to item_catalog.db.
        """
        
        engine = create_engine("sqlite:///item_catalog.db")
        Base.metadata.bind = engine
        self.DBSession = sessionmaker(bind=engine)
    
    
    def create_item(self, item):
        """Persist a new item to the database."""
        
        session = self.DBSession()
        session.add(item)
        session.commit()
        
        
    def edit_item(self, item):
        """Edit the properties of an existing item in the database."""
        
        session = self.DBSession()
        
        item_to_edit = self.get_item(item.id, session)
        item_to_edit.name = item.name
        
        session.add(item_to_edit)
        session.commit()
        
        
    def delete_item(self, item):
        """Delete an item from the database."""
        
        session = self.DBSession()
        
        item_to_delete = self.get_item(item.id, session)
        
        session.delete(item_to_delete)
        session.commit()
    
    
    def get_items(self):
        """Get all items in the database."""
        
        session = self.DBSession()
        return session.query(Item).all()
    
    
    def get_item(self, item_id, session = None):
        """Get a specific item in the database by id."""
        
        if session is None:
            session = self.DBSession()
        
        try:
            return session.query(Item).filter_by(id = item_id).one()
        except NoResultFound:
            return None


def test_create_item(item_dao):
    
    item = Item()
    item.name = "Nintendo Switch"
    
    item_dao.create_item(item)
    
    
def test_get_items(item_dao):
    
    items = item_dao.get_items()
    
    assert len(items) == 1
    assert items[0].name == "Nintendo Switch"
    
    
def test_get_item(item_dao):
    
    item = item_dao.get_item(1)
    
    assert item.name == "Nintendo Switch"
    
    
def test_get_item_with_no_result_found(item_dao):
    
    item = item_dao.get_item(100)
    
    assert item is None
    
    
def test_edit_item(item_dao):
    
    item = Item()
    item.id = 1
    item.name = "SNES Classic"
    
    item_dao.edit_item(item)
    
    assert item_dao.get_item(1).name == "SNES Classic"
    
    
def test_delete_item(item_dao):
    
    item = Item()
    item.id = 1
    
    item_dao.delete_item(item)
    
    assert item_dao.get_item(1) is None
    
    
if __name__ == "__main__":
    
    #os.remove("item_catalog.db")
    item_dao = ItemDao()
    
    test_create_item(item_dao)
    test_get_items(item_dao)
    test_get_item(item_dao)
    test_get_item_with_no_result_found(item_dao)
    test_edit_item(item_dao)
    test_delete_item(item_dao)
    