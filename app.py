from flask import Response, jsonify, request
from PlaneModel import Plane
from settings import app
import json
import re

DEFAULT_PAGE_LIMIT = 3


def validPlaneObject(planeObject):
    if ("id" in planeObject and "description" in planeObject and
            "datetime" in planeObject and "longitude" in planeObject and
            "latitude" in planeObject and "elevation"in planeObject):
        return True
    else:
        return False


def check_if_string(variable):
    if isinstance(variable, str):
        return True
    else:
        return False


def check_if_float(variable):
    if isinstance(variable, float) or isinstance(variable, int):
        return True
    else:
        return False


def check_if_date_time(variable):
    regex = r"""^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|
            [12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)
            ?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"""
    match_iso8601 = re.compile(regex, re.VERBOSE)
    try:
        if match_iso8601.match(variable) is not None:
            return True
    except ValueError:
        return False
    return False


@app.route("/planes", methods=["GET"])
def get_planes():
    if request.args.get("pagination") and request.args["pagination"] == "true":
        print("here")
        use_pagination = True
        if request.args.get("page"):
            page = request.args["page"]
        else:
            page = 1
        if request.args.get("limit"):
            limit = request.args["limit"]
        else:
            limit = DEFAULT_PAGE_LIMIT
        page = int(page)
        limit = int(limit)
        if page < 1:
            page = 1
    else:
        use_pagination = False
        page = 1
        limit = DEFAULT_PAGE_LIMIT
    result = Plane.get_planes(use_pagination, page, limit)
    planes = jsonify({"planes": result})
    return planes


@app.route("/planes/<string:unique_id>", methods=["GET"])
def get_plane_by_unique_id(unique_id):
    return_value = Plane.get_plane(unique_id)
    if str(return_value) == "None":
        errorMsg = {"error": "unique_id not found"}
        response = Response(json.dumps(errorMsg), status=404,
                            mimetype="application/json")
        return response
    else:
        return jsonify(return_value)


@app.route("/planes", methods=["POST"])
def add_plane():
    request_data = request.get_json()
    if (not check_if_string(request_data["id"]) or
            not check_if_string(request_data["description"]) or
            not check_if_date_time(request_data["datetime"]) or
            not check_if_float(request_data["longitude"]) or
            not check_if_float(request_data["latitude"]) or
            not check_if_float(request_data["elevation"])):
        invalidPlaneObjectErrorMessage = {
            "error": "Invalid data type in request"
            }
        response = Response(json.dumps(invalidPlaneObjectErrorMessage),
                            400, mimetype="application/json")
        return response
    unique_id = request_data["id"] + request_data["datetime"]
    exists = Plane.get_plane(unique_id)
    if str(exists) != "None":
        invalidPlaneObjectErrorMessage = {
            "error": "Plane already exists for same date/time"
            }
        response = Response(json.dumps(invalidPlaneObjectErrorMessage), 400,
                            mimetype="application/json")
        return response
    if (validPlaneObject(request_data)):
        Plane.add_plane(request_data["id"], request_data["description"],
                        request_data["datetime"], request_data["longitude"],
                        request_data["latitude"], request_data["elevation"])
        response = Response("", 201, mimetype="application/json")
        response.headers["Location"] = "/planes/" + str(unique_id)
        return response
    else:
        invalidPlaneObjectErrorMessage = {
            "error": "Invalid plane object passed in request"
            }
        response = Response(json.dumps(invalidPlaneObjectErrorMessage), 400,
                            mimetype="application/json")
        return response


@app.route("/planes/<string:unique_id>", methods=["PUT"])
def replace_plane(unique_id):
    request_data = request.get_json()
    if (not check_if_string(request_data["id"]) or
            not check_if_string(request_data["description"]) or
            not check_if_date_time(request_data["datetime"]) or
            not check_if_float(request_data["longitude"]) or
            not check_if_float(request_data["latitude"]) or
            not check_if_float(request_data["elevation"])):
        invalidPlaneObjectErrorMessage = {
            "error": "Invalid data type in request"
            }
        response = Response(json.dumps(invalidPlaneObjectErrorMessage),
                            400, mimetype="application/json")
        return response
    if (validPlaneObject(request_data)):
        is_successful = Plane.delete_plane(unique_id)
        if (not is_successful):
            errorMsg = {"error": "Plane does not exist for date/time"}
            response = Response(json.dumps(errorMsg), status=404,
                                mimetype="application/json")
            return response
        else:
            Plane.add_plane(request_data["id"],
                            request_data["description"],
                            request_data["datetime"],
                            request_data["longitude"],
                            request_data["latitude"],
                            request_data["elevation"])
            response = Response("", 201, mimetype="application/json")
            response.headers["Location"] = "/planes/" + str(unique_id)
            return response
    else:
        invalidPlaneObjectErrorMessage = {
            "error": "Invalid plane object passed in request"
            }
        response = Response(json.dumps(invalidPlaneObjectErrorMessage), 400,
                            mimetype="application/json")
        return response


@app.route("/planes/<string:unique_id>", methods=["DELETE"])
def delete_plane(unique_id):
    is_successful = Plane.delete_plane(unique_id)
    if (is_successful):
        response = Response("", status=204)
    else:
        errorMsg = {"error": "Plane does not exist for date/time"}
        response = Response(json.dumps(errorMsg), status=404,
                            mimetype="application/json")
    return response


app.run(port=5000)
