from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Ecommerce App")

# Upgraded inventory with images and more products
PRODUCTS = {
    1: {"name": "Pro Laptop", "price": 1200, "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&q=80"},
    2: {"name": "Smartphone X", "price": 899, "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80"},
    3: {"name": "Smart Watch", "price": 250, "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&q=80"},
    4: {"name": "4K Ultra TV", "price": 950, "image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&q=80"},
    5: {"name": "Noise-Cancelling Headphones", "price": 300, "image": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400&q=80"},
    6: {"name": "Mechanical Keyboard", "price": 130, "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=400&q=80"},
}
cart = {}

class CartItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/products")
def get_products():
    return PRODUCTS

@app.post("/cart")
def add_to_cart(item: CartItem):
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
    return {"message": "Success"}

@app.get("/cart")
def view_cart():
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return {"items": cart, "total": total}

@app.post("/checkout")
def checkout():
    global cart
    if not cart:
        raise HTTPException(status_code=400, detail="Your cart is empty!")
    cart.clear()
    return {"message": "Payment successful! Thank you for your order."}
