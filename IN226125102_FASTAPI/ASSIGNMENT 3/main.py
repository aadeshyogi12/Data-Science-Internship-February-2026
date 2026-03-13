from fastapi import FastAPI, Response, status

app = FastAPI()

# initial products list
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# helper function
def find_product(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


# get all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

#audit
@app.get("/products/audit")
def product_audit():

    in_stock = []
    out_stock = []

    for p in products:
        if p["in_stock"]:
            in_stock.append(p)
        else:
            out_stock.append(p)

    total_value = 0
    for p in in_stock:
        total_value += p["price"] * 10

    expensive = products[0]
    for p in products:
        if p["price"] > expensive["price"]:
            expensive = p

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_names": [p["name"] for p in out_stock],
        "total_stock_value": total_value,
        "most_expensive": {
            "name": expensive["name"],
            "price": expensive["price"]
        }
    }

#bonus
from fastapi import Query

@app.put("/products/discount")
def apply_discount(category: str = Query(...), discount_percent: int = Query(...)):

    updated_products = []

    for p in products:
        if p["category"] == category:
            new_price = int(p["price"] * (1 - discount_percent / 100))
            p["price"] = new_price
            updated_products.append(p)

    if len(updated_products) == 0:
        return {
            "message": f"No products found in category: {category}"
        }

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated_products),
        "updated_products": updated_products
    }


# get single product
@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    return product


# add product
@app.post("/products")
def add_product(product: dict, response: Response):

    for p in products:
        if p["name"] == product["name"]:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product already exists"}

    next_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": next_id,
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "in_stock": product.get("in_stock", True)
    }

    products.append(new_product)

    response.status_code = status.HTTP_201_CREATED

    return {
        "message": "Product added",
        "product": new_product
    }


# update product
@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None, response: Response = None):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    if price is not None:
        product["price"] = price

    if in_stock is not None:
        product["in_stock"] = in_stock

    return {
        "message": "Product updated",
        "product": product
    }


# delete product
@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)

    return {
        "message": f"Product '{product['name']}' deleted"
    }