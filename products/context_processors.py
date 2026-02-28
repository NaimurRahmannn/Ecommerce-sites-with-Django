from products.models import Category


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


def sidebar_categories(request):
    men_categories = Category.objects.filter(category_type='MEN').order_by('categroy_name')
    women_categories = Category.objects.filter(category_type='WOMEN').order_by('categroy_name')
    return {
        "men_categories": men_categories,
        "women_categories": women_categories,
    }
