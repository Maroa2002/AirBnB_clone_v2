#!/usr/bin/python3
"""database storage engine"""
from sqlalchemy import create_engine
from os import getenv
from models.city import City
from models.state import State
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session

user = getenv("HBNB_MYSQL_USER")
password = getenv("HBNB_MYSQL_PWD")
host = getenv("HBNB_MYSQL_HOST")
database = getenv("HBNB_MYSQL_DB")
env_var = getenv("HBNB_ENV")

class DBStorage:
    """New storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(f"mysql+mysqldb://{user}:{password}\
                                      @{host}/{database}", pool_pre_ping=True)
        if env_var == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Querying objects"""
        from models import classes
        objs_dict = {}
        if cls:
            query = self.__session.query(classes[cls]).all()
            for obj in query:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                objs_dict[key] = obj
        else:
            for cls in classes.values():
                query = self.__session.query(cls).all()
                for obj in query:
                    key = '{}.{}'.format(type(obj).__name__, obj.id)
                    objs_dict[key] = obj
        return objs_dict

    def new(self, obj):
        """add object to current database session"""
        self.__storage.add(obj)

    def save(self):
        """commit all changes of current database session"""
        self.__storage.commit()

    def delete(self, obj=None):
        """delete from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables and current db session"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()
