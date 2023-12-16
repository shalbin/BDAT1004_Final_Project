from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)


MONGO_URI = "mongodb+srv://shalbin13:hE9iW1z6vfM9ieva@cluster0.v4etain.mongodb.net/?retryWrites=true&w=majority"  # Replace with your MongoDB URI
client = MongoClient(MONGO_URI)
db = client.get_database("StockDB")
collection = db["AAPL"]


# Route to get all items
@app.route('/api/items', methods=['GET'])
def get_all_items():
    items = list(collection.find())

    # Convert ObjectId to string for each item in the list
    for item in items:
        item['_id'] = str(item['_id'])

    return jsonify(items)




@app.route('/api/items/range', methods=['GET'])
def get_items_range():
    start = int(request.args.get('start', 0))
    end = int(request.args.get('end', 3))
    items = list(collection.find()[start:end])
    items_dict = [{"_id": str(item["_id"]), "other_key": item.get("other_key", "")} for item in items]

    return jsonify(items_dict)



@app.route('/api/items/<item_id>', methods=['GET'])
def get_item_by_id(item_id):
    item = collection.find_one({"_id": item_id})
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
