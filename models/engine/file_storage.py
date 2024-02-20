#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            filtered_objs = {}
            for key, obj in self.__objects.items():
                if type(obj) == cls:
                    filtered_objs[key] = obj
            return filtered_objs
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
          #  temp.update(FileStorage.__objects)
            for key, val in self.__objects.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls = val['__class__']
                    cls_model = classes.get(cls)
                    if cls_model:
                        key = "{}.{}".format(cls, val['id'])
                        self.__objects[key] = cls_model(**val)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            temp = {}

    def delete(self, obj=None):
        """delete obj from __objects if inside """
        if obj is not None:
            key = "{}:{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()
        else:
            pass
