class Product:
    produc_sku = None
    price = None
    img_url = None
    product_name = None

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            self.product_sku = kwargs["product_sku"]
            self.price = kwargs["price"]
            self.img_url = kwargs.get("img_url", None)
            self.product_name = kwargs["product_name"]
        else:
            self.build_object(args[0])

    def build_object(self, json_dict):
        self.product_sku = json_dict["product_sku"]
        self.price = json_dict["price"]
        self.img_url = json_dict["img_url"]
        self.product_name = json_dict["product_name"]


class Order:
    details = []
    customer_name = None
    order_id = None
    paid_at_date = None
    paid_at_time = None
    trained = False

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            self.customer_name = kwargs["customer_name"]
            self.order_id = kwargs["order_id"]
            self.paid_at_date = kwargs["paid_at_date"]
            self.paid_at_time = kwargs["paid_at_time"]
        else:
            self.build_object(args[0])

    def build_object(self, json_dict):
        self.customer_name = json_dict["customer_name"]
        self.order_id = json_dict["order_id"]
        self.paid_at_date = json_dict["paid_at_date"]
        self.paid_at_time = json_dict["paid_at_time"]
        self.details = []

        for item in json_dict["items"]:
            if item.strip():
                detail = Order_Detail(order_id=self.order_id, product_sku=item)
                self.details.append(detail)


class Order_Detail:
    order_id = None
    product_sku = None
    order_detail_id = None
    quantity = 1

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            self.order_id = kwargs["order_id"]
            self.product_sku = kwargs["product_sku"]
        else:
            self.build_object(args[0])

    def build_object(self, json_dict):
        self.quantity = json_dict["quantity"]
        self.product_sku = json_dict["product_sku"]
