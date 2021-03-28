import csv
from sqldb import sqldb
from models import Order,Order_Detail

data = []

with open('Datasets/orders.csv') as file:
    reader = csv.DictReader(file)
    data = list(reader)

temp = {}

data = [dict(i) for i in data]

for row in data:
    if row["Financial Status"] == "paid":
        if len(temp) > 0:
            order = Order(temp)
            sqldb.add_order(order)
            for detail in order.details:
                sqldb.add_order_details(detail)
        
        timestamp = row["Paid at"].split()
        temp = {
            "order_id":row["Name"][1:],
            "paid_at_time":timestamp[1],
            "paid_at_date":timestamp[0],
            "customer_name":row["Billing Name"],
            "items":[row["Lineitem sku"]]
        }
    else:
        temp["items"].append(row["Lineitem sku"])