from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product


def _get_cart(request):
    return request.session.get("cart", [])


def _save_cart(request, cart):
    request.session["cart"] = cart
    total = 0
    for item in cart:
        try:
            total += int(item.get("quantity", 0))
        except (TypeError, ValueError):
            continue
    request.session["cart_count"] = total
    request.session.modified = True


def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        return render(request, "product/product.html", context={"product": product})
    except Exception as e:
        print(e)


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        qty_raw = request.POST.get("quantity", "1")
        try:
            quantity = int(qty_raw)
        except ValueError:
            quantity = 1
        if quantity < 1:
            quantity = 1
        size = request.POST.get("select_size") or ""
    else:
        quantity = 1
        size = request.GET.get("size", "")

    if product.size_variant.exists() and not size:
        messages.error(request, "Please select a size before adding to cart.")
        next_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
        if next_url:
            return redirect(next_url)
        return redirect("get_product", slug=product.slug)

    cart = _get_cart(request)
    for item in cart:
        if item.get("product_id") == str(product.pk) and item.get("size", "") == size:
            item["quantity"] = item.get("quantity", 0) + quantity
            _save_cart(request, cart)
            next_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
            if next_url:
                return redirect(next_url)
            return redirect("get_product", slug=product.slug)

    cart.append({"product_id": str(product.pk), "quantity": quantity, "size": size})
    _save_cart(request, cart)
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
    if next_url:
        return redirect(next_url)
    return redirect("get_product", slug=product.slug)


def cart(request):
    cart = _get_cart(request)
    cart_items = []
    subtotal = 0

    for item in cart:
        product = Product.objects.filter(pk=item.get("product_id")).first()
        if not product:
            continue
        quantity = item.get("quantity", 1)
        line_total = product.price * quantity
        subtotal += line_total
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "size": item.get("size", ""),
                "line_total": line_total,
            }
        )

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": subtotal,
    }
    return render(request, "product/cart.html", context)


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    size = request.GET.get("size", "")
    cart = _get_cart(request)
    new_cart = []

    for item in cart:
        if item.get("product_id") == str(product.pk) and item.get("size", "") == size:
            continue
        new_cart.append(item)

    _save_cart(request, new_cart)
    return redirect("cart")


def update_cart(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

    product_id = request.POST.get("product_id", "")
    size = request.POST.get("size", "")
    qty_raw = request.POST.get("quantity", "1")
    try:
        quantity = int(qty_raw)
    except ValueError:
        quantity = 1

    cart = _get_cart(request)
    updated = False

    new_cart = []
    for item in cart:
        if item.get("product_id") == product_id and item.get("size", "") == size:
            updated = True
            if quantity > 0:
                item["quantity"] = quantity
                new_cart.append(item)
            continue
        new_cart.append(item)

    if not updated and quantity > 0:
        new_cart.append({"product_id": product_id, "quantity": quantity, "size": size})

    _save_cart(request, new_cart)

    subtotal = 0
    line_total = 0
    cart_count = 0

    for item in new_cart:
        product = Product.objects.filter(pk=item.get("product_id")).first()
        if not product:
            continue
        item_qty = item.get("quantity", 1)
        cart_count += item_qty
        subtotal += product.price * item_qty
        if item.get("product_id") == product_id and item.get("size", "") == size:
            line_total = product.price * item_qty

    return JsonResponse(
        {
            "success": True,
            "removed": quantity <= 0,
            "line_total": line_total,
            "subtotal": subtotal,
            "total": subtotal,
            "cart_count": cart_count,
        }
    )


def buy_now(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        qty_raw = request.POST.get("quantity", "1")
        size = request.POST.get("select_size") or ""
    else:
        qty_raw = request.GET.get("quantity", "1")
        size = request.GET.get("size", "")

    try:
        quantity = int(qty_raw)
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    if product.size_variant.exists() and not size:
        messages.error(request, "Please select a size before Buy now.")
        return redirect("get_product", slug=product.slug)

    line_total = product.price * quantity
    subtotal = line_total
    context = {
        "checkout_items": [
            {
                "product": product,
                "quantity": quantity,
                "size": size,
                "line_total": line_total,
            }
        ],
        "subtotal": subtotal,
        "shipping": 0,
        "total": subtotal,
        "back_url": "get_product",
        "back_url_kwargs": {"slug": product.slug},
    }
    return render(request, "product/checkout.html", context)


def checkout(request):
    cart = _get_cart(request)
    checkout_items = []
    subtotal = 0

    for item in cart:
        product = Product.objects.filter(pk=item.get("product_id")).first()
        if not product:
            continue
        quantity = item.get("quantity", 1)
        line_total = product.price * quantity
        subtotal += line_total
        checkout_items.append(
            {
                "product": product,
                "quantity": quantity,
                "size": item.get("size", ""),
                "line_total": line_total,
            }
        )

    if not checkout_items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    context = {
        "checkout_items": checkout_items,
        "subtotal": subtotal,
        "shipping": 0,
        "total": subtotal,
        "back_url": "cart",
    }
    return render(request, "product/checkout.html", context)
