from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy


engine = create_engine("sqlite:///puppies.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

print("\nPuppies in alphabetical order")
for puppy in session.query(Puppy).order_by(Puppy.name).all():
    print(puppy.name)

print("\nPuppies that are less than 6 months old ordered by youngest first")
for puppy in session.query(Puppy).filter(Puppy.date_of_birth > '2017-01-06').order_by(Puppy.date_of_birth).all():
    print("{0} - {1}".format(puppy.name, puppy.date_of_birth))

print("\nPuppies ordered by weight")
for puppy in session.query(Puppy).order_by(Puppy.weight).all():
    print("{0} - {1}".format(puppy.name, puppy.weight))

print("\nPuppies by shelter")
for puppy in session.query(Puppy).join(Puppy.shelter).order_by(Shelter.name, Puppy.name).all():
    print("{0} - {1}".format(puppy.shelter.name, puppy.name))

session.close()
