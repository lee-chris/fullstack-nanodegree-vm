import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "id"      : self.id,
            "name"    : self.name,
            "email"   : self.email,
            "picture" : self.picture
        }


class Category(Base):
    """Item category.
    
    Within the catalog, the items will be grouped by Category.
    """
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    
    items = relationship("Item", backref="categories")
    
    @property
    def serialize(self):
        
        return {
            "id" : self.id,
            "name" : self.name,
            "user_id" : self.user_id
        }
    
    @property
    def serialize_full(self):
        
        return {
            "id" : self.id,
            "name" : self.name,
            "user_id" : self.user_id,
            "items" : [item.serialize for item in self.items]
        }
    
    
    def __str__(self):
        return "Category: {0}, {1}".format(self.id, self.name)
    

class Item(Base):
    """Item in the catalog."""
    
    __tablename__ = "items"
    
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    description = Column(String(250))
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(Category)
    
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    
    @property
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "description" : self.description,
            "category_id" : self.category_id,
            "user_id" : self.user_id
        }
    
    
    def __str__(self):
        return "Item: {0}, {1}".format(self.id, self.name)


engine = create_engine("sqlite:///item_catalog.db")

Base.metadata.create_all(engine)