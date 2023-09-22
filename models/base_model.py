#!/usr/bin/python3
"""This is the base model class for AirBnB"""
from sqlalchemy.ext.declarative import declarative_base
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BaseModel:
    """This class defines all common attributes/methods for other classes"""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string"""
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """Return a string representation"""
        return self.__str__()

    def save(self):
        """Updates the public instance attribute updated_at to current"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Creates a dictionary of the class and returns it"""
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        # Remove _sa_instance_state if it exists
        my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """Deletes the current instance from storage"""
        models.storage.delete(self)
