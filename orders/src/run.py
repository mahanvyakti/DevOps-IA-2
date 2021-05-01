from faker import Faker
from flask import Flask, jsonify, request
import logging
import random
import json


app = Flask(__name__)
data = []
fake = Faker()


@app.route('/allOrders', methods=['GET'])
def all_orders():
    return jsonify(data), 200


@app.route('/order/<int:orderId>', methods=['GET'])
def get_order(orderId):
    search_result = list(filter(lambda order: order['id'] == orderId, data))
    if search_result == [] or search_result is None:
        return {'error':'Order Not Found!'}, 200
    
    found_order = search_result[0]
    print(found_order)
    return jsonify(found_order), 200


@app.route('/custSearch', methods=['GET'])
def cust_search():
    json = request.get_json()
    name = json.get('name', '')
    result = [order for order in data if name in order['cust']]
    return jsonify(result), 200


def create_order(num):
    return {
        'id': num,
        'cust': fake.name(),
        'items': [random.randint(1, 100) for _ in range(1, random.randint(1, 10))]
    }


def create_data():
    with open('../static/customer.json', "r") as f:
        data = json.load(f)
        return data

@app.route('/add_order', methods=['POST'])
def add_order():
    print("Retrieving params")
    json = request.get_json()
    cust = json.get('cust', '')
    id = json.get('id', '')
    items = json.get('items', [])
    new_order=  {'cust':cust, 'id':id, 'items':items}
    print(new_order)
    data.append(new_order)
    # result = [order for order in data if name in order['cust']]
    return jsonify(new_order), 200


@app.route('/delete/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    print("Deleting Order")
    search_result = list(filter(lambda order: order['id'] == order_id, data))
    if search_result == [] or search_result is None:
        print("Empty search result")
        return {'error':'Order Not Found!'}, 200
    
    found_order = search_result[0]
    print(found_order)
    
    try:
        data.remove(found_order)
    except ValueError as e:
        print("Remove throwed value error")
        return {'error':'Order Not Found!'}, 200
    print("Order deleted")
    return found_order, 200


if __name__ == '__main__':
    data = create_data()
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, port=5001)
