#!/usr/bin/python3
"""database storage engine"""
from sqlalchemy import create_engine, MetaData
from os import getenv
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import Base, BaseModel
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }

class DBStorage:
    """New storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)


        Base.metadata.create_all(self.__engine)
        #if getenv("HBNB_ENV") == 'test':
            #Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Querying objects"""
        if not self.__session:
            self.reload()

        objects = {}
        if isinstance(cls, str):
            cls = classes.get(cls, None)

        query_classes = [cls] if cls else classes.values()

        for query_cls in query_classes:
            for obj in self.__session.query(query_cls):
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj

        return objects

    def new(self, obj):
        """add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables and current db session"""
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()

    def close(self):
        """method to to call remove method"""
        self.__session.close()
