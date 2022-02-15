from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime
from app.configs.database import db
from datetime import datetime
import re

@dataclass
class Lead(db.Model):
  date = datetime.now()

  __tablename__ = "leads"

  id = Column(Integer, primary_key = True)
  name: str = Column(String, nullable = False)
  email: str = Column(String, unique = True, nullable = False)
  phone: str = Column(String, unique = True, nullable = False)
  creation_date: str = Column(DateTime, default = date)
  last_visit: str = Column(DateTime, default = date)
  visits: int = Column(Integer, default = 1)

  @staticmethod
  def sort_by_visits(leads: list):
    """
      Sort a lead list by visits.\n
      Returning a sorted list.
    """

    def sort_list(e):
      return e["visits"]

    leads.sort(key = sort_list)

    return leads

  @staticmethod
  def check_phone_number(phone: str):
    """
      Check the phone format from a string.\n
      Returning an error message, a correct phone format and the phone given.
    """

    valid_phone = re.fullmatch(r"^\([\d]{2}\)[\d]{5}\-[\d]{4}$", phone)

    if not valid_phone or len(phone) != 14:
      return {
        "error": "Invalid phone number",
        "valid_phone": "(xx)xxxxx-xxxx",
        "phone": phone
      }

    return {}

  @staticmethod
  def check_keys_or_values(data: dict, check_value: bool = False):
    """
      Check keys or values.\n
      Check a dict(Lead) from the request body if the keys or values are correct.
    """

    keys = ["name", "email", "phone"]
    values_type = {"name": "string", "email": "string", "phone": "string"}

    if check_value:
      invalids = {}

      for key in data.keys():
        if type(data[key]) != str:
          invalids[key] = str(type(data[key]))[8:-2]

      return {"invalid_values": invalids, "correct_values": values_type}

    else:
      invalids = []

      for key in data.keys():
        if not key in keys:
          invalids.append(key)

      return {"invalid_keys": invalids, "avaliable_keys": keys}

  @staticmethod
  def check_missing_keys(data: dict):
    """
      Check missing keys.\n
      This function receives a dict(data) from the request body.
    """

    keys = ["name", "email", "phone"]
    missing_keys = []

    for key in keys:
      if not data.get(key):
        missing_keys.append(key)
    
    if len(missing_keys) < 3:
      return {"missing_keys": missing_keys, "avaliable_key": keys}

    return {}