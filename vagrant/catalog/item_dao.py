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
        
        self.engine = create_engine("sqlite:///item_catalog.db")
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
    
    
    def close(self):
        
        self.engine.dispose()
    
    
    def create_item(self, item):
        """Persist a new item to the database."""
        
        session = self.DBSession()
        session.add(item)
        session.commit()
        session.refresh(item)
        session.close()
        
        return item
        
        
    def edit_item(self, item):
        """Edit the properties of an existing item in the database."""
        
        session = self.DBSession()
        
        item_to_edit = self.get_item(item.id, session = session)
        item_to_edit.name = item.name
        
        session.add(item_to_edit)
        session.commit()
        session.close()
        
        
    def delete_item(self, item):
        """Delete an item from the database."""
        
        session = self.DBSession()
        
        item_to_delete = self.get_item(item.id, session = session)
        
        session.delete(item_to_delete)
        session.commit()
        session.close()
    
    
    def get_items(self):
        """Get all items in the database."""
        
        session = self.DBSession()
        items = session.query(Item).all()
        session.close()
        
        return items
    
    
    def get_item(self, item_id, session = None):
        """Get a specific item in the database by id."""
        
        is_session_open = False
        
        if session is not None:
            is_session_open = True
        
        if is_session_open == False:
            session = self.DBSession()
        
        item = None
        try:
            item = session.query(Item).filter_by(id = item_id).one()
        except NoResultFound:
            item = None
        
        if is_session_open == False:
            session.close()
        return item
    
    
    def create_category(self, category):
        """Create a new product category."""
        
        session = self.DBSession()
        session.add(category)
        session.commit()
        session.refresh(category)
        session.close()
        
        return category


    def get_categories(self):
        """Get all product categories."""
        
        session = self.DBSession()
        categories = session.query(Category).all()
        
        session.close()
        return categories


    def get_category(self, category_id, session = None):
        """Get a specific category."""
        
        is_session_open = False
        if session is not None:
            is_session_open = True
        
        if is_session_open == False:
            session = self.DBSession()
        
        category = None
        try:
            category = session.query(Category).filter_by(id = category_id).one()
        except NoResultFound:
            category = None
        
        if is_session_open == False:
            session.close()
        
        return category
    
    
    def edit_category(self, category_to_edit):
        """Edit a category."""
        
        session = self.DBSession()
        
        category = self.get_category(category_to_edit.id, session = session)
        
        category.name = category_to_edit.name
        session.add(category)
        session.commit()
        session.refresh(category)
        session.close()
        
        return category
    
    
    def delete_category(self, category_to_delete):
        """Delete a category."""
        
        session = self.DBSession()
        
        category = self.get_category(category_to_delete.id, session = session)
        session.delete(category)
        session.commit()
        session.close()
        
        return category


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

def test_create_category(item_dao):
    
    category = Category()
    
    category.id = 1
    category.name = "Video Games"
    
    item_dao.create_category(category)


def test_get_categories(item_dao):
    
    categories = item_dao.get_categories()
    
    assert len(categories) == 1
    assert categories[0].name == "Video Games"


def test_get_category(item_dao):
    
    category = item_dao.get_category(1)
    
    assert category is not None
    assert category.name == "Video Games"


def test_edit_category(item_dao):
    
    category = Category()
    
    category.id = 1
    category.name = "Video Game Consoles"
    
    item_dao.edit_category(category)
    
    category = item_dao.get_category(1)
    
    assert category is not None
    assert category.name == "Video Game Consoles"

    
def test_delete_category(item_dao):
    
    category = Category()
    category.id = 1
    
    item_dao.delete_category(category)
    
    category = item_dao.get_category(1)
    
    assert category is None
    
    
if __name__ == "__main__":
    
    item_dao = ItemDao()
    
    test_create_item(item_dao)
    test_get_items(item_dao)
    test_get_item(item_dao)
    test_get_item_with_no_result_found(item_dao)
    test_edit_item(item_dao)
    test_delete_item(item_dao)
    
    test_create_category(item_dao)
    test_get_categories(item_dao)
    test_get_category(item_dao)
    test_edit_category(item_dao)
    test_delete_category(item_dao)
    
    item_dao.close()
    os.remove("item_catalog.db")
  