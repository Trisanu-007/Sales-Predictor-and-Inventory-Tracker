import csv
import random
import time

from models import Order
from models import Order_Detail
from models import Product
from rich.progress import Progress
from sqldb import sqldb

data = []

with open("Datasets/orders.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

data = [dict(i) for i in data]

with Progress() as progress:
    products = {i["Lineitem sku"]: i["Lineitem name"] for i in data}
    task1 = progress.add_task("[cyan]Adding orders..", total=len(data))
    task2 = progress.add_task("[green]Adding products..", total=len(products))
    temp = {}

    for row in data:
        if row["Financial Status"] == "paid":
            if len(temp) > 0:
                order = Order(temp)
                sqldb.add_order(order)
                for detail in order.details:
                    if detail.product_sku.isnumeric():
                        sqldb.add_order_details(detail)
                        print(detail.order_id)
                        time.sleep(0.02)
                temp = {}

            timestamp = row["Paid at"].split()
            temp = {
                "order_id": row["Name"][1:],
                "paid_at_time": timestamp[1],
                "paid_at_date": timestamp[0],
                "customer_name": row["Billing Name"],
                "items": [row["Lineitem sku"]],
            }
        else:
            temp["items"].append(row["Lineitem sku"])
        progress.update(task1, advance=1)

    for sku, name in products.items():
        if not sku.isnumeric():
            continue
        price = round(2.5 + random.normalvariate(5.0, 1.5), 2)
        product = Product(product_sku=sku, product_name=name, price=price)
        sqldb.add_product(product)
        progress.update(task2, advance=1)
