from flask import jsonify, Response
from bson.json_util import dumps


def create_response(message, status, data=None):
    if data is not None:
        try:
            return jsonify({"message": message, "status": status, "data": data}), status
        except TypeError:
            serialized_data = dumps(
                {"message": message, "status": status, "data": data}
            )
            return Response(serialized_data, status=status, mimetype="application/json")
    else:
        return jsonify({"message": message, "status": status}), status
