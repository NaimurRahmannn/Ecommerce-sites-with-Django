def cart_count(request):
    total = request.session.get("cart_count")
    if total is None:
        cart = request.session.get("cart", [])
        total = 0
        for item in cart:
            try:
                total += int(item.get("quantity", 0))
            except (TypeError, ValueError):
                continue
    return {"cart_count": total}
