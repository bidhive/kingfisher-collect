from flask import Flask, json, jsonify
from flask_cors import CORS, cross_origin
from utils import read_dirs, format_item, ItemManager

# Setup
items = ItemManager()
contracts = read_dirs("data/australia_sample")
items.set_items(contracts)

# Flask
app = Flask(__name__)
CORS(app)


def by_index(index: int):
    if index < 0 or index > len(items.items):
        return "Index out of bounds"

    return items.items[index]


def response(message: str, error=False):
    return {"error" if error else "message": message}


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    data = {"items": len(items.items)}
    return app.response_class(response=data, status=200, mimetype="application/json")


@app.route("/all", methods=["GET"])
@cross_origin()
def all():
    data = json.dumps(items.items)
    return app.response_class(response=data, status=200, mimetype="application/json")


@app.route("/<index>", methods=["GET"])
@cross_origin()
def retrieve(index):
    index = int(index)
    if index < 0 or index > len(items.items):
        return app.response_class(
            response={"error": "Index out of bounds"},
            status=200,
            mimetype="application/json",
        )
    item = by_index(index)

    return app.response_class(response=item, status=200, mimetype="application/json")


@app.route("/<index>/<key>", methods=["GET"])
@cross_origin()
def attribute(index: str, key: str):
    index = int(index)
    item = by_index(index)

    data = json.dumps(item.get(key))
    return app.response_class(response=data, status=200, mimetype="application/json")


@app.route("/<index>/<key>/last", methods=["GET"])
@cross_origin()
def last(index: str, key: str):
    index = int(index)
    item = by_index(index)

    attribute = item.get(key, None)

    if attribute == None:
        return app.response_class(
            response={"error": "Invalid attribute"},
            status=400,
            mimetype="application/json",
        )
    elif not isinstance(attribute, list):
        return app.response_class(
            response={"error": "Attribute is not a list"},
            status=400,
            mimetype="application/json",
        )

    get_index = max(len(attribute) - 1, 0)
    data = attribute[get_index]
    return app.response_class(response=data, status=200, mimetype="application/json")


@app.route("/<index>/<key>/<item_index>", methods=["GET"])
@cross_origin()
def key_by_index(index: str, key: str, item_index: str):
    index = int(index)
    item = by_index(index)

    attribute = item.get(key, None)

    if attribute == None:
        return app.response_class(
            response={"error": "Invalid attribute"},
            status=400,
            mimetype="application/json",
        )
    elif not isinstance(attribute, list):
        return app.response_class(
            response={"error": "Attribute is not a list"},
            status=400,
            mimetype="application/json",
        )

    get_index = int(item_index)

    if get_index < 0 or get_index > len(attribute):
        return app.response_class(
            response={"error": "Attribute item index out of bounds"},
            status=400,
            mimetype="application/json",
        )

    data = attribute[item_index]
    return app.response_class(response=data, status=200, mimetype="application/json")


@app.route("/first", methods=["GET"])
@cross_origin()
def first():
    if len(items.items) == 0:
        return app.response_class(
            response={"error": "No data"}, status=400, mimetype="application/json"
        )

    data = items.items[0]
    return app.response_class(response=data, status=200, mimetype="application/json")
