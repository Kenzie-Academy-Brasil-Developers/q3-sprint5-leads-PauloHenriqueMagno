import re

class UniqueViolationError(Exception):
  """ 
    Violation of unique value.\n
    Is necessary the error message from database to create a new error message.
  """
  
  def __init__(self, message):
    error = message.split()[-3]
    error = re.sub(r"[\)\(]", "", error, 3)
    error = re.sub("\)$", "", error, 1)
    error = re.sub("=", " ", error)
 
    self.message = f"{error} has already been taken."
