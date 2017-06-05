from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

cheesepizza = session.query(MenuItem).filter_by(id = 1).one()
cheesepizza.price = "$2.99"
session.add(cheesepizza)
session.commit()

# for testing
test = session.query(MenuItem).filter_by(id = 1).one()
print(test.price)
