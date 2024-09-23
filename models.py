from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    email = Column(String)
    phone = Column(String)
    cell = Column(String)
    date_of_birth = Column(String) # Check Date type
    age = Column(String)

    location = relationship("Location", back_populates="user", uselist=False)
    login = relationship("Login", back_populates="user", uselist=False)
    picture = relationship("Picture", back_populates="user", uselist=False)

class Location(Base):
    __tablename__ = 'locations'
    
    location_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    street_name = Column(String)
    street_number = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postcode = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    
    user = relationship("User", back_populates="location")

class Login(Base):
    __tablename__ = 'logins'
    
    login_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    uuid = Column(String)
    username = Column(String)
    password = Column(String)
    salt = Column(String)
    md5 = Column(String)
    sha1 = Column(String)
    sha256 = Column(String)
    
    user = relationship("User", back_populates="login")

class Picture(Base):
    __tablename__ = 'pictures'
    
    picture_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    large = Column(String)
    medium = Column(String)
    thumbnail = Column(String)
    
    user = relationship("User", back_populates="picture")