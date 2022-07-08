from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Order
from .forms import ProductForm, OrderForm

def counts():
    orders_count = Order.objects.all().count()
    products_count = Product.objects.all().count()
    workers_count = User.objects.all().count()
    return orders_count, products_count, workers_count


@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count, products_count, workers_count = counts()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def staff(request):
    workers = User.objects.all()
    orders_count, products_count, workers_count = counts()
    context = {
        'workers': workers,
        'workers_count': workers_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/staff.html', context)


@login_required
def staff_detail(request, pk):
    worker = User.objects.get(id=pk)
    context = {
        'worker': worker,
    }
    return render(request, 'dashboard/staff_detail.html', context)


@login_required
def product(request):
    items = Product.objects.all()
    orders_count, products_count, workers_count = counts()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            form.save()
            return redirect('dashboard-product')

    else:
        form = ProductForm()
    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/product.html', context)


@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')


@login_required
def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard-index')
    return render(request, 'dashboard/order_delete.html')


@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/product_update.html', context)


@login_required
def order_update(request, pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=item)
        # user = User.objects.get(id=item.staff.id)
        # print(user.username)
        # print(user.is_superuser)
        # if request.user.is_authenticated:
        #     print("User is logged in :)")
        print(f"Logged Username --> {request.user.username}")
        loggeduser = request.user.username
        if form.is_valid():
            form.save()
            if loggeduser == 'Manager':
                return redirect('dashboard-order')
            else:
                return redirect('dashboard-index')
    else:
        form = OrderForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/order_update.html', context)


@login_required
def order(request):
    orders = Order.objects.all()
    orders_count, products_count, workers_count = counts()
    context = {
        'orders': orders,
        'workers_count': workers_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/order.html', context)
