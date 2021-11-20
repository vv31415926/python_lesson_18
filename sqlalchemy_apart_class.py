from sqlalchemy import Column, Integer, String, Float, create_engine,Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, create_session

from sqlalchemy.orm import scoped_session
from sqlalchemy.pool import NullPool

engine = create_engine( 'sqlite:///apartment.db', echo=False , poolclass=NullPool )
Base = declarative_base()
metadata = MetaData( bind=engine  )


class View_apartment( Base ):
    __table__ = Table('View_apartment', metadata, autoload=True)

    def __init__(self, npp, colname, coltitle):
        md = metadata
        self.npp = npp
        self.colname = colname
        self.coltitle = coltitle

    def __str__(self):
        return f'{self.coltitle}'


class Region(Base):
    __table__ = Table('Region', metadata, autoload=True)

    def __init__(self, name, id_city):
        self.name = name
        self.id_country = id_city

    def __str__(self):
        return f'{self.name}'


class City(Base):
    __table__ = Table('City', metadata, autoload=True)

    def __init__(self, name, id_country):
        self.name = name
        self.id_country = id_country

    def __str__(self):
        return f'{self.name}'


class Country(Base):
    __table__ = Table('Country', metadata, autoload=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'


class Address(Base):
    __table__ = Table('Address', metadata, autoload=True)

    def __init__(self, id_region, id_city, name):
        self.id_region = id_region
        self.id_city = id_city
        self.name = name

    def __str__(self):
        return f'{self.name}'


class Characteristic(Base):
    __table__ = Table('Characteristic', metadata, autoload=True)

    def __init__(self, id_address, data):
        self.id_address = id_address
        self.data = data

    def __str__(self):
        return f'{self.data}'


Session = sessionmaker( bind=engine )
session = Session()

#session_factory = sessionmaker(bind=engine)
#Session = scoped_session(session_factory)
#session = Session()


class SQLAlchemy_apartment:
    @classmethod
    def get_field(self):
        #print('============ Поля просмотра =======================')
        lst_field = session.query(View_apartment).all()
        lst=[]
        for field in lst_field:
            #print(field.colname, field.coltitle, sep=', ')
            lst.append( {'npp':field.npp, 'name':field.colname, 'title':field.coltitle} )
        #print('***********************')
        #print(lst)
        lst = sorted(  lst, key=lambda x: x['npp']  )  # сортировка по порядку
        #print(lst)
        #print('***********************')
        return lst

    @classmethod
    def get_country(self):
        query = session.query(City, Country)
        query = query.join(City, City.id_country == Country.id)
        records = query.all()
        lst=[]
        dic = {}
        for city, country in records:
            #print(city, country, sep=', ')
            lst.append( {'city':city, 'country':country} )
        return lst

    @classmethod
    def get_region(self, name):
        reg = session.query(Region).filter( Region.name == name).first()
        t = type( reg )
        lst = [reg.id, reg.name, reg.id_city, reg.date]

        return lst

    @classmethod
    def get_data(self, region):
        reg = self.get_region( region )
        id_reg = reg[0]
        upd = reg[3]

        query = session.query( Characteristic, Address ).filter( Address.id_region == id_reg )
        query = query.join( Address, Address.id == Characteristic.id_address )
        records = query.all()
        for char, address in records:
            print( address, char,  sep='; ')
        return (records, upd)