from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Ecommerce App")

# Your original data structures
PRODUCTS = {
    1: {"name": "Laptop", "price": 10000},
    2: {"name": "Smartphone", "price": 5000},
    3: {"name": "Watch", "price": 1000},
    4: {"name": "TV", "price": 2000},
}
cart = {}

# Validates data coming from the frontend
class CartItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serves the HTML frontend to the browser."""
    with open("index.html", "r") as f:
        return f.read()

@app.get("/products")
def get_products():
    """Replaces display_products()"""
    return PRODUCTS

@app.post("/cart")
def add_to_cart(item: CartItem):
    """Replaces add_to_cart()"""
    if item.product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Invalid product ID!")
    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")

    if item.product_id in cart:
        cart[item.product_id]["quantity"] += item.quantity
    else:
        cart[item.product_id] = {
            "name": PRODUCTS[item.product_id]["name"],
            "price": PRODUCTS[item.product_id]["price"],
            "quantity": item.quantity,
        }

    return {"message": f"Added {item.quantity} x {PRODUCTS[item.product_id]['name']} to your cart!"}

@app.get("/cart")
def view_cart():
    """Replaces view_cart()"""
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return {"items": cart, "total": total}

@app.post("/checkout")
def checkout():
    """Replaces checkout() and cart_clear()"""
    global cart
    if not cart:
        raise HTTPException(status_code=400, detail="Your cart is empty! Add items before checking out.")
    
    cart.clear()
    return {"message": "Thank you for shopping with us!"}
