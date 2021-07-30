from flask import Flask, Response, stream_with_context, jsonify, request
from datetime import datetime
import time
import uuid
import random
import json

APP = Flask(__name__)

def generate_updated_at(iterator):
    ut = int("1463288494") + iterator
    return datetime.fromtimestamp(ut).isoformat()


@APP.route("/sync_data/<int:rowcount>", methods=["POST"])
def post_sync_request(rowcount):
    return APP.response_class()


@APP.route("/get_table_metadata", methods=["POST"])
def get_table_metadata():
    if request.method == 'POST':
        table_names = [
            {'id': 0,
            'name': 'ACCOUNT',
            'nrows': 5000},
            {'id': 1,
            'name': 'USER',
            'nrows': 1000
            },
            {'id': 2,
            'name': 'CONTACT',
            'nrows': 100
            }
        ]
        return jsonify(table_names)


@APP.route("/user/<int:rowcount>", methods=["GET"])
def get_large_request(rowcount):
    """Returns N rows of data"""
    def f():
        """Generator"""
        for _i in range(rowcount):
            time.sleep(.01)
            pk_id = _i+1
            txid = uuid.uuid4()
            uid = uuid.uuid4()
            amount = round(random.uniform(-1000, 1000), 2)
            updated_at = generate_updated_at(_i)
            yield f"({pk_id}, '{txid}', '{uid}'', {amount}, {updated_at})"
    return APP.response_class(stream_with_context(f()), mimetype='application/json')


@APP.route("/account/<int:rowcount>", methods=["GET"])
def get_small_request(rowcount):
    """Returns N rows of data"""
    def f():
        """Generator"""
        for _i in range(rowcount):
            time.sleep(.01)
            pk_id = _i+1
            txid = uuid.uuid4()
            uid = uuid.uuid4()
            amount = round(random.uniform(-1000, 1000), 2)
            updated_at = generate_updated_at(_i)
            yield f"({pk_id}, '{txid}', '{uid}'', {amount}, {updated_at})"
    return APP.response_class(stream_with_context(f()), mimetype='application/json')


@APP.route("/contact/<int:start_row>/<int:final_row>", methods=["GET"])
def get_contacts(start_row, final_row):
    """Returns N rows of static_response"""
    with open("static_response.json", "r") as f:
        data = json.load(f)
    if request.method == "GET":
        response_data = list(data)[start_row-1:final_row]
        return jsonify(response_data)


if __name__ == "__main__":
    APP.run(debug=True)