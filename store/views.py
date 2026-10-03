from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "store/detail.html", {"product": product})

def add_to_cart(request, id):
    cart = request.session.get("cart", {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session["cart"] = cart
    return redirect("cart")

def cart(request):
    cart_data = request.session.get("cart", {})
    items = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })
        total += subtotal

    return render(request, "store/cart.html", {
        "items": items,
        "total": total
    })


def checkout(request):
    cart_data = request.session.get("cart", {})
    if not cart_data:
        return redirect("cart")

    total = 0
    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=product_id)
        total += product.price * quantity

    from .models import Order
    order = Order.objects.create(total=total)
    request.session["cart"] = {}

    return render(request, "store/success.html", {"order": order})

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "store/signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        auth_login(request, user)
        return redirect("home")

    return render(request, "store/signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("home")

        return render(request, "store/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "store/login.html")


def user_logout(request):
    auth_logout(request)
    return redirect("home")
