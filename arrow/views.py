from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination

from .forms import *
from .serializers import *


# Authentication
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'arrow/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'arrow/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


# Main Page
def home_view(request):
    return render(request, 'arrow/home.html')


def portfolio_view(request):
    return render(request, 'arrow/portfolio.html')


# User
def addUser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/showUsers')
            except:
                pass
    else:
        form = UserForm()
    return render(request, 'arrow/addUser.html', {'form': form})


def showUsers(request):
    # if request.user.is_authenticated:
    #     users = User.objects.all()
    #     return render(request, 'arrow/showUsers.html', {'users': users})
    # else:
    #     return redirect('/')

    if request.user.is_authenticated:
        sort = request.GET.get('sort', '')
        desc = request.GET.get('desc', False)
        user = User.objects.all()

        # Getting search request
        ctx = {}
        url_parameter = request.GET.get("q")

        if url_parameter:
            users = user.filter(First_Name__istartswith=url_parameter)
        else:
            users = user

        # sorting
        if sort:
            if desc:
                users = users.order_by("-" + sort)

            else:
                users = users.order_by(sort)

        # Pagination
        page = request.GET.get('page', 1)

        paginator = Paginator(users, 3)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        ctx["desc"] = desc
        ctx["users"] = users
        ctx["q"] = url_parameter
        ctx["sorts"] = sort

        # ajax call
        if request.is_ajax():
            html = render_to_string(
                template_name="arrow/showUsersfile.html",
                context={'desc': desc, 'users': users, 'q': url_parameter, 'sorts': sort}
            )

            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)

        return render(request, "arrow/showUsers.html", context=ctx)
    else:
        return redirect('/')


def editUser(request, id):
    user = User.objects.get(id=id)
    return render(request, 'arrow/editUser.html', {'user': user})


def updateUser(request, id):
    user = User.objects.get(id=id)
    form = UserForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        return redirect("/showUsers")
    return render(request, 'arrow/editUser.html', {'user': user})


def destroyUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/showUsers")


# Product
def addProduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/showProducts')
            except:
                pass
    else:
        form = ProductForm()
    return render(request, 'arrow/addProduct.html', {'form': form})


def showProducts(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        return render(request, 'arrow/showProducts.html', {'products': products})
    else:
        return redirect('/')


def editProduct(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'arrow/editProduct.html', {'product': product})


def updateProduct(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("/showProducts")

    form = ProductForm(instance=product)

    return render(request, 'arrow/editProduct.html', {'product': form, 'id': id})


def destroyProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("/showProducts")


# Rest Framework
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UsersViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['^First_Name', '^Last_Name']
    ordering_fields = ['First_Name', 'Last_Name']


class ProductsViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['^Product_Category', '^Product_Name']
    ordering_fields = ['Product_Category', 'Product_Name']
