import datetime

from sqlalchemy.schema import Table, MetaData
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, create_session

engine = create_engine( 'sqlite:///apartment.db', echo=True )
Base = declarative_base()

metadata = MetaData( bind=engine )


class City( Base ):
    __table__ = Table('city', metadata, autoload=True )
    # def __init__(self, name: str):
    #     self.name = name
    #
    # def __str__(self):
    #     return f'{self.name}'

class Country( Base ):
    __table__ = Table( 'country', metadata, autoload=True )
    # def __init__(self, name:str ):
    #     self.name = name
    #
    # def __str__(self):
    #     return f'{self.name}'

session = create_session( bind=engine )

#print( '------------------------------------------' )
#lst_country = session.query( Country ).all()

print( '------------------------------------------' )
lst_city = session.query( City ).all()



# for city in lst_city:
#     country = session.query(Country).filter_by( id = city.id_country ).first()
#     print( country.name, city.name )