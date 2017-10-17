import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    """Item category.
    
    Within the catalog, the items will be grouped by Category.
    """
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    

class Item(Base):
    """Item in the catalog."""
    
    __tablename__ = "items"
    
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(Category)


engine = create_engine("sqlite:///item_catalog.db")

Base.metadata.create_all(engine)