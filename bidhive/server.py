from flask import Flask
from utils import read_dirs, format_item, ItemManager

# Setup
items = ItemManager()
contracts = read_dirs("data/australia_sample")
items.set_items(contracts)

# Flask
app = Flask(__name__)


@app.route("/")
def index():
    return str(len(items.items))


@app.route("/<index>")
def retrieve(index):
    index = int(index)
    if index < 0 or index > len(items.items):
        return "Index out of bounds"

    item = items.items[index]
    return item


@app.route("/first")
def first():
    if len(items.items) == 0:
        return "None"

    return str(items.items[0])
