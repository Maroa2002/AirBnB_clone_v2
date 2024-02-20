#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from os import getenv

class Amenity(BaseModel):
    name = ""
    if getenv("HBNB_TYPE_STORAGE") == "db":
        pass
