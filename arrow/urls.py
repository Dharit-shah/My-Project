from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

# API
router.register(r'users', views.UsersViewSet)
router.register(r'products', views.ProductsViewSet)


urlpatterns = [
    # REST framework
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Authentication
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logouts'),

    # Main Page
    path('', views.home_view),
    path('portfolio', views.portfolio_view),

    # User
    path('addUser', views.addUser),
    path('showUsers/', views.showUsers),
    path('editUser/<int:id>', views.editUser),
    path('updateUser/<int:id>', views.updateUser),
    path('deleteUser/<int:id>', views.destroyUser),

    # Product
    path('addProduct', views.addProduct),
    path('showProducts/', views.showProducts),
    path('editProduct/<int:id>', views.editProduct),
    path('updateProduct/<int:id>', views.updateProduct),
    path('deleteProduct/<int:id>', views.destroyProduct),
]
