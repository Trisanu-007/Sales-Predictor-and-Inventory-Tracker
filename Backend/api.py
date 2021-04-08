from flask import Flask
from flask import request
from models import Order
from models import Order_Detail
from models import Product
from sqldb import sqldb

app = Flask(__name__)


@app.route("/order/<int:order_id>", methods=["GET", "POST", "DELETE"])
def crud_order(order_id=None):
    if request.method == "POST":
        data = request.json(force=True)

        order = Order(data)

        sqldb.add_order(order)
        sqldb.add_order_details(order)

    elif request.method == "GET":
        sqldb.get_order(order_id)

    elif request.method == "DELETE":
        sqldb.delete_order(order_id)


@app.route("/order/bulk", methods=["POST", "DELETE"])
def bulk_order():
    if request.method == "POST":
        data_list = request.json(force=True)
        for data in data_list:
            order = Order(data)

            sqldb.add_order(order)
            sqldb.add_order_details(order)
    elif request.method == "DELETE":
        for data in data_list:
            sqldb.delete_order(data)


@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.json(force=True)
    product = Product(data)
    sqldb.add_product(product)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
