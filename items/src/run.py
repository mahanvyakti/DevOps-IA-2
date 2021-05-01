from flask import Flask, jsonify, request
import logging
import json


app = Flask(__name__)
data = []

def find_item_by_id(id):
    return list(filter(lambda item: item['id'] == id, data))

@app.route('/allItems', methods=['GET'])
def all_items():
    return jsonify(data), 200


@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    search_result = find_item_by_id(item_id)
    
    if search_result == [] or search_result is None:
        print("Empty search result")
        return {'error':'Item Not Found!'}, 200
    
    found_item = search_result[0]
    print(found_item)
    return jsonify(found_item), 200

@app.route('/item/<int:item_id>', methods=['POST'])
def add_item(item_id):
    print("Retrieving params")
    json = request.get_json()
    desc = json.get('desc', '')
    
    search_result = find_item_by_id(item_id)
    print()
    if search_result == [] or search_result is None:
        new_item=  {'id':item_id, 'desc':desc}
        print(new_item)
        data.append(new_item)
        return jsonify(new_item), 200 
    
    return {'error':'Item with given id already exists!'}, 200

def create_data():
    with open('../static/items.json', "r") as f:
        data = json.load(f)
        return data


if __name__ == '__main__':
    data = create_data()
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, port=5002)
