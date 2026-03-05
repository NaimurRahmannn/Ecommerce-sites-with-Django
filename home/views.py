from django.shortcuts import render
from products.models import Product



def index(request):
    sort = request.GET.get('sort', 'default')
    products = Product.objects.all()
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    context = {'products': products, 'current_sort': sort}
    return render(request, 'home/index.html', context)


def contact(request):
    return render(request, 'home/contact.html')