from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

products = [
    {"id":1,"name":"Wireless Mouse","price":499,"category":"Electronics","in_stock":True},
    {"id":2,"name":"Notebook","price":99,"category":"Stationery","in_stock":True},
    {"id":3,"name":"USB Hub","price":799,"category":"Electronics","in_stock":False},
    {"id":4,"name":"Pen Set","price":49,"category":"Stationery","in_stock":True}
]

orders = []
feedback = []


# ------------------------------------------------
# Q1 filter products
# ------------------------------------------------

@app.get("/products/filter")
def filter_products(category: str = None,
                    max_price: int = None,
                    min_price: int = None):

    data = products

    if category:
        data = [p for p in data if p["category"].lower() == category.lower()]

    if max_price:
        data = [p for p in data if p["price"] <= max_price]

    if min_price:
        data = [p for p in data if p["price"] >= min_price]

    return {"products": data}


# ------------------------------------------------
# Q2 product price
# ------------------------------------------------

@app.get("/products/{product_id}/price")
def product_price(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return {"name": p["name"], "price": p["price"]}

    return {"error": "Product not found"}


# ------------------------------------------------
# Q3 feedback
# ------------------------------------------------

class CustomerFeedback(BaseModel):

    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


@app.post("/feedback")
def add_feedback(data: CustomerFeedback):

    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }


# ------------------------------------------------
# Q4 summary
# ------------------------------------------------

@app.get("/products/summary")
def summary():

    total = len(products)

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    expensive = max(products, key=lambda x: x["price"])
    cheap = min(products, key=lambda x: x["price"])

    cat = list(set([p["category"] for p in products]))

    return {
        "total_products": total,
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {"name": expensive["name"], "price": expensive["price"]},
        "cheapest": {"name": cheap["name"], "price": cheap["price"]},
        "categories": cat
    }


# ------------------------------------------------
# Q5 bulk order
# ------------------------------------------------

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem]


@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):

    ok = []
    failed = []
    total = 0

    for item in order.items:

        prod = None
        for p in products:
            if p["id"] == item.product_id:
                prod = p
                break

        if not prod:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
            continue

        if not prod["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": prod["name"] + " is out of stock"})
            continue

        sub = prod["price"] * item.quantity
        total += sub

        ok.append({
            "product": prod["name"],
            "qty": item.quantity,
            "subtotal": sub
        })

    return {
        "company": order.company_name,
        "confirmed": ok,
        "failed": failed,
        "grand_total": total
    }


# ------------------------------------------------
# bonus
# ------------------------------------------------

class OrderRequest(BaseModel):
    product_id: int
    quantity: int


@app.post("/orders")
def place_order(order: OrderRequest):

    new = {
        "order_id": len(orders) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending"
    }

    orders.append(new)

    return new


@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for o in orders:
        if o["order_id"] == order_id:
            return {"order": o}

    return {"error": "Order not found"}


@app.patch("/orders/{order_id}/confirm")
def confirm(order_id: int):

    for o in orders:
        if o["order_id"] == order_id:
            o["status"] = "confirmed"
            return {"message": "Order confirmed", "order": o}

    return {"error": "Order not found"}