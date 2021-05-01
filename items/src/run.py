from faker import Faker
from flask import Flask, jsonify
import logging
import json


app = Flask(__name__)
data = []
fake = Faker()


@app.route('/allItems', methods=['GET'])
def all_orders():
    return jsonify(data), 200


@app.route('/item/<int:num>', methods=['GET'])
def get_order(num):
    return jsonify(data[num]), 200


def create_items(num):
    return {
        'id': num,
        'desc': fake.bs()
    }


def create_data():
    with open('../static/items.json', "r") as f:
        data = json.load(f)
        return data
    # return [create_items(num) for num in range(1, 100)]


if __name__ == '__main__':
    data = create_data()
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, port=5002)
