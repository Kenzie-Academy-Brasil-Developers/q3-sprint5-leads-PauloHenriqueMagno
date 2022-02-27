from flask import jsonify, current_app, request
from app.models.leads_model import Lead
from datetime import datetime
from psycopg2.errors import InvalidParameterValue, NullValueNotAllowed, NoDataFound
from sqlalchemy.exc import IntegrityError
from app.exceptions.unique_violation_error import UniqueViolationError

def get_leads():
  """ Get all leads. """
  try:
    leads = Lead.query.all()

    if len(leads) == 0:
      raise NoDataFound()

    serializer = [
      {
        "id": lead.id,
        "name": lead.name,
        "email": lead.email,
        "phone": lead.phone,
        "creation_date": lead.creation_date,
        "last_visit": lead.last_visit,
        "visits": lead.visits
      } for lead in leads
    ]

    serializer = Lead.sort_by_visits(serializer)

    return jsonify(serializer), 200

  except NoDataFound:
    return jsonify({"error": "leads list is empty"}), 404

def creat_lead():
  """ Create a new lead. """

  try:
    data = dict(request.json)

    error = Lead.check_missing_keys(data)

    if len(error.get("missing_keys")) > 0:
      raise NullValueNotAllowed(error)

    error = Lead.check_keys_or_values(data)

    if len(error.get("invalid_keys")) > 0:
      raise InvalidParameterValue(error)

    error = Lead.check_keys_or_values(data, True)

    if len(error.get("invalid_values")) > 0:
      raise ValueError(error)

    error = Lead.check_phone_number(data["phone"])

    if error.get("error"):
      raise ValueError(error)

    lead = Lead(**data)

    current_app.db.session.add(lead)
    current_app.db.session.commit()

    return jsonify(lead), 201

  except IntegrityError as err:
    try:
      if "already exists" in err.args[0]:
        raise UniqueViolationError(err.args[0]) from err

      return jsonify({"error": err.args[0]}), 400

    except UniqueViolationError as err:
      return jsonify({"error": err.message}), 409

  except NullValueNotAllowed as err:
    return jsonify({"error": err.args[0]}), 400

  except ValueError as err:
    return jsonify(err.args[0]), 400

  except InvalidParameterValue as err:
    return jsonify(err.args[0]), 400


def modify_lead():
  """
    Modify lead.
  """

  try:
    data = dict(request.json)
    date_now = datetime.now()

    email = data.get("email")

    if not email:
      raise NullValueNotAllowed("email is necessary")

    error = Lead.check_keys_or_values(data)

    if len(error.get("invalid_keys")) > 0:
      raise InvalidParameterValue(error)

    error = Lead.check_keys_or_values(data, True)

    if len(error.get("invalid_values")) > 0:
      raise ValueError(error)

    lead: Lead = Lead.query.filter(Lead.email == email).first()

    if not lead:
      raise NoDataFound("Not found")

    for key, value in data.items():
      setattr(lead, key, value)

    setattr(lead, "visits", (lead.visits+1))
    setattr(lead, "last_visit", date_now)

    current_app.db.session.add(lead)
    current_app.db.session.commit()

    return jsonify(lead), 200

  except IntegrityError as err:
    try:
      if "already exists" in err.args[0]:
        raise UniqueViolationError(err.args[0]) from err

      return jsonify({"error": err.args[0]}), 400

    except UniqueViolationError as err:
      return jsonify({"error": err.message}), 409

  except NoDataFound as err:
    return jsonify({"error": err.args[0]}), 404

  except NullValueNotAllowed as err:
    return jsonify({"error": err.args[0]}), 400

  except ValueError as err:
    return jsonify({"error": err.args[0]}), 400


def delete_lead():
  """
    Delete lead.
  """

  try:
    data = dict(request.json)

    email = data.get("email")

    if not email:
      raise NullValueNotAllowed("email is necessary")
    if type(email) != str:
      raise TypeError("email have to be string")

    lead = Lead.query.filter(Lead.email == email).first()

    if not lead:
      raise NoDataFound("Not found")

    current_app.db.session.delete(lead)
    current_app.db.session.commit()

    return jsonify(), 204

  except TypeError as err:
    return jsonify({"error": err.args[0]}), 400

  except NullValueNotAllowed as err:
    return jsonify({"error": err.args[0]}), 400

  except NoDataFound as err:
    return jsonify({"error": err.args[0]}), 404