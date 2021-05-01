from flask import Flask, jsonify, request
import logging
import requests

app = Flask(__name__)

@app.route('/detail/<int:order_id>', methods=['GET'])
def detail(order_id):
    try:
        print("Called orders")
        if order_id < 1:
            print("Order id < 1!")
            return {'error':'Order Not Found!'}, 200
        order = requests.get('http://localhost:5001/order/{}'.format(order_id)).json()
        print("Got orders")
        if "error" in order:
            return order, 200
        
        items = [_fetch_item(item_id-1) for item_id in order.get('items', [])]
        print("Found these items")
        print(items)
        del order['items']
        order['items'] = items
        return jsonify(order), 200
    except Exception as e:
        print(e)
        return e


def _fetch_item(item_id):
    print("searching ", item_id, " ..." )
    return requests.get('http://localhost:5002/item/{}'.format(item_id)).json()


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, port=5003)
