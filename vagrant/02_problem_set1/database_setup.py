import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Float

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):

    __tablename__ = "shelter"

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address = Column(String(100))
    city = Column(String(100))
    state = Column(String(3))
    zip_code = Column(String(10))
    website = Column(String(100))


class Puppy(Base):

    __tablename__ = "puppy"

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    date_of_birth = Column(String(100))
    gender = Column(String(1))
    weight = Column(Float)
    shelter_id = Column(Integer, ForeignKey("shelter.id"))
    picture = Column(String(100))

    shelter = relationship(Shelter)
        

####### insert at end of file #######

engine = create_engine("sqlite:///puppies.db")

Base.metadata.create_all(engine)
