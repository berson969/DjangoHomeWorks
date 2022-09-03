from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):

    template = 'catalog.html'
    sort_pages = request.GET.get('sort')
    phones_all = Phone.objects.all()
    if sort_pages == 'name':
        phones_all = phones_all.order_by('name')
    elif sort_pages == 'min_price':
        phones_all = phones_all.order_by('price')
    elif sort_pages == 'max_price':
        phones_all = phones_all.order_by('-price')
    context = {
        'phones': phones_all,
    }
    return render(request, template, context)


def show_product(request, slug):
    phone = Phone.objects.filter(slug__contains=slug).first()
    template = 'product.html'
    context = {
        'phone': phone,
    }
    return render(request, template, context)
