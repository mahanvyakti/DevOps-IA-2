from flask import Flask, json, jsonify, request
import logging
import requests


app = Flask(__name__)


@app.route('/orders', methods=['GET'])
def orders():
    count = request.args.get('count')
    data = requests.get('http://localhost:5001/allOrders').json()
    if count:
        return jsonify(data[:int(count)]), 200
    else:
        return jsonify(data), 200


@app.route('/detail/<int:order_id>', methods=['GET'])
def detail(order_id):
    data = requests.get('http://localhost:5003/detail/{}'.format(order_id)).json()
    return jsonify(data), 200


@app.route('/custSearch/<string:name>', methods=['GET'])
def cust_search(name):
    payload = {'name': name}
    data = requests.get('http://localhost:5001/custSearch', json=payload).json()
    return jsonify(data), 200

@app.route('/add_order', methods=['POST'])
def add_order():
    payload = request.get_json(force=True)
    print(payload)
    cust = payload.get('cust', '')  
    id = payload.get('id', '')
    items = payload.get('items', [])
    new_order =  {'cust':cust, 'id':id, 'items':items}

    print("Posting....")
    data = requests.post('http://localhost:5001/add_order', json=new_order).json()
    print('Posted!')

    return jsonify(data), 200

@app.route('/item/<int:item_id>', methods=['POST'])
def add_item(item_id):
    payload = request.get_json(force=True)
    print(payload)
    
    desc = payload.get('desc', '')  
    new_item =  {'desc':desc, 'id':item_id,}
    print("Posting....")
    data = requests.post('http://localhost:5002/item/{}'.format(item_id), json=new_item).json()
    print('Posted!')

    return jsonify(data), 200

@app.route('/delete/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    data = requests.delete('http://localhost:5001/delete/{}'.format(order_id)).json()
    return jsonify(data), 200


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, port=5000)
