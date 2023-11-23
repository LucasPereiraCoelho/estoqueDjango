from django.shortcuts import render, redirect
from .models import Products, Categories
from random import randint
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(redirect_field_name='login')
def index(request):
    produtos = Products.objects.filter(in_stock=True, user_id=request.user.id)
    return render(request, 'pages/index.html', {'produtos':produtos})

def stockless(request):
    produtos = Products.objects.filter(in_stock=False)
    return render(request, 'pages/index.html', {'produtos':produtos})

def search_product(request):
    q = request.GET.get('q')
    produtos = Products.objects.filter(name__icontains=q, in_stock=True)
    return render(request, 'pages/index.html', {'produtos':produtos})

def add_product(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        cod = randint(100, 10000)
        category = request.POST.get('category')
        picture = request.FILES.get('picture')
        price = request.POST.get('price')
        description = request.POST.get('description')
        qtd = request.POST.get('qtd')
        discount = request.POST.get('discount')
        created_at = datetime.now()
        if int(qtd) > 0:
            in_stock = True
        else:
            in_stock = False

        Products.objects.create(
            user_id=request.user.id,
            name=name, category_id=category, picture=picture, cod=cod, price=price,
            description=description, qtd=qtd, discount=discount, created_at=created_at,
            in_stock=in_stock
        )

        return redirect('home')

    else:
        categories = Categories.objects.all()
        return render(request, 'pages/add-product.html', {'categories':categories}) 

def delete_product(request, id):
    product = Products.objects.get(id=id)
    product.delete()
    return redirect ('home')

def sell_product(request, id):
    product = Products.objects.get(id=id)
    product.qtd -= 1
    if product.qtd == 0:
        product.in_stock = False
    if product.qtd < 0:
        product.qtd = 0
    product.save()
    return redirect ('product-detail', id)

def product_detail(request, id):
    product = Products.objects.get(id=id)
    return render(request, 'pages/product_detail.html', {'product':product})