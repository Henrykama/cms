from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter
from.decorators import unathenticated_user, allowed_users,admin_only
from django.contrib.auth.models import User


@unathenticated_user
def registerPage(request):

        form= CreateUserForm()

        if request.method =='POST':
            form = CreateUserForm(request.POST)
            if form.is_valid:
                user =form.save()
                username = form.cleaned_data.get('username')
                ''' group = Group.objects.get(name= 'customer')
                user.groups.add(group) '''
                messages.success(request, "Account created" +  username)
                return redirect('login')
        else:  
            context= {
                'form': form
            }
            return render(request, 'accounts/register.html', context)
@unathenticated_user
def loginPage(request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username= username, password= password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
                
        context={}

        return render(request, 'accounts/login.html', context)
@login_required(login_url = 'login')

def userprofile(request):
    context={

    }

    return render(request, 'accounts/user_profile.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['customer'])


def accountsSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance = customer) 
    context={
        'form':form
    }

    return render(request, 'accounts/account_settings.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required(login_url = 'login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers= Customer.objects.all()
    total_customers= customers.count()
    total_orders= orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context= {

        'orders': orders,
        'customers':customers,
        'delivered':delivered,
        'pending':pending,
        'total_orders': total_orders,
        'total_customers': total_customers
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])


def products(request):

    products= Product.objects.all()
    context= {

        'products': products
    }
    return render(request,'accounts/products.html', context)
@login_required(login_url = 'login')

@allowed_users(allowed_roles=['admin'])

def customers(request, pk_id):
    customer = Customer.objects.get(id= pk_id)
    customer_orders= customer.order_set.all()

    myfilter = OrderFilter(request.GET, queryset=customer_orders)
    customer_orders= myfilter.qs
    context={
        'customer':customer,
        'customer_orders': customer_orders,
        'myfilter': myfilter
    }
    return render(request,'accounts/customers.html', context)
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])

def createOrders(request, pk_id):
    OrderFormSet= inlineformset_factory(Customer, Order, fields=('product','status'))

    customer = Customer.objects.get(id=pk_id)

    formset =OrderFormSet(queryset=Order.objects.none(),instance=customer)
 
    if request.method =='POST': 
     
        formset =OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')

    context= {
        'formset':formset

    }

    return render(request,'accounts/order_form.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])


def updateOrder(request, pk_id):
    form = OrderForm()

    order= Order.objects.get(id=pk_id)
    form = OrderForm(instance=order)

    if request.method =='POST': 
     
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={
        'form':form
    }
    return render(request,'accounts/order_form.html',context)
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])

def deleteOrder(request, pk_id):

    order= Order.objects.get(id=pk_id)
    if request.method =='POST':
        order.delete()
        return redirect('/')


    context= {
        'order':order

    }
    return render(request,'accounts/delete.html', context)


