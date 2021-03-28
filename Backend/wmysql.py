import mysql.connector
import logging
import time
import random

from models import Product,Order,Order_Detail

is_local_test_instance = True

class wmysql():
    # wmysql(host='127.0.0.1', user='', passwd='', database='')
    def __init__(self, host=None, **kwargs):
        self.mydb = mysql.connector.connect(
            **kwargs,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            use_unicode=True)

    def execute_tuple(self, sql, args):
        logging.info("Executing SQL: " + sql)
        self.mydb.start_transaction()
        c = self.mydb.cursor()
        c.execute(sql, args)
        if self.mydb.unread_result:
            res = c.fetchall()
        else:
            res = []
        self.mydb.commit()
        c.close()
        return res

    def execute_many(self, sql, args_list):
        logging.info("Executing many SQL: " + sql)
        self.mydb.start_transaction()
        c = self.mydb.cursor()
        c.executemany(sql, args_list)
        if self.mydb.unread_result:
            res = c.fetchall()
        else:
            res = []
        self.mydb.commit()
        c.close()
        return res

    def execute(self, sql, *args):
        return self.execute_tuple(sql, args)



class sql_queries():
    wsql = None
    allow_editing = False
    allow_deleting = False

    def __init__(self, allow_editing = False, allow_deleting = False):
        self.allow_editing = allow_editing
        if allow_editing:
            self.allow_deleting = allow_deleting
        else:
            self.allow_deleting = False

        self.wsql = wmysql(host='127.0.0.1', user='analyst', passwd='xIHG0MMZOe1pN7VGfQ47aV', database='icps')

        if not self.allow_deleting:
            self.wsql.execute("SET SESSION sql_mode = 'STRICT_ALL_TABLES'")

        self.setup_tables()

    def declare_table(self, table_name, cols_list, extra_decl = []):
        args_str = ', '.join(cols_list + extra_decl)

        # Create SQL commands - NOTE - This is safe only because we are using constant strings
        # Don't have something stupid like input-defined table names
        rtable_sql = "CREATE TABLE IF NOT EXISTS {} ({}) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(table_name, args_str)

        # Execute SQL
        self.wsql.execute(rtable_sql)


    def setup_tables(self):
        self.declare_table("orders", [
            "customer_name VARCHAR(50) NOT NULL",
            "order_id SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY",
            "paid_at_date VARCHAR(5) NOT NULL",
            "paid_at_time VARCHAR(5) NOT NULL",
            "trained BOOLEAN DEFAULT FALSE"
        ])
    
        self.declare_table("order_details",[
            "order_detail_id SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY",
            "order_id SMALLINT NOT NULL",
            "product_sku MEDIUMINT NOT NULL",
        ])

        self.declare_table("products",[
            "product_sku MEDIUMINT NOT NULL PRIMARY KEY",
            "price TINYINT NOT NULL",
            "img_url TEXT CHARACTER SET latin1 NOT NULL",
            "product_name TEXT CHARACTER SET latin1 NOT NULL",
        ])

    def add_product(self,product:Product):
        self.wsql.execute("INSERT INTO products (product_sku,price,img_url,product_name) VALUES (%s,%s,%s,%s)",product.produc_sku,product.price,product.img_url,product.product_name)

    def add_order(self,order:Order):
        self.wsql.execute("INSERT INTO orders (customer_name,order_id,paid_at_date,paid_at_time,trained) VALUES (%s,%s,%s,%s,%s)",order.customer_name,order.order_id,order.paid_at_date,order.paid_at_time,order.trained)

    def add_order_details(self,order_detail:Order_Detail):
        self.wsql.execute("INSERT INTO order_details (order_detail_id,order_id,product_sku) VALUES (%s,%s,%s)",order_detail.order_detail_id,order_detail.order_id,order_detail.product_sku)

    def get_order(self,order_id):
        result = self.wsql.execute("SELECT * FROM orders WHERE order_id=%s",order_id)[0] 
        order_data = dict(zip(("customer_name","order_id","paid_at_date","paid_at_time","trained"),result)) 
        
        order_details = self.get_order_details(order_id)
        order_data.update({"items":order_details})
        
        return order_data
    
    def get_order_details(self,order_id):
        return self.wsql.execute("SELECT * FROM order_details WHERE order_id=%s",order_id)

    def delete_order(self,order_id):
        self.wsql.execute("DELETE FROM orders WHERE order_id=%s",order_id)
        self.wsql.execute("DELETE FROM order_details WHERE order_id=%s",order_id)


if __name__ == "__main__":
    sqldb = sql_queries()