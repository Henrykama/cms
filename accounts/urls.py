from django.urls import path
from . import views

urlpatterns = [


   path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('user-profile/', views.userprofile, name= 'user-profile'),

    path('account/', views.accountsSettings, name='account_setting'),
    
   path('', views.home, name='home'),
   path('products/', views.products, name='products'),
   path('customers/<str:pk_id>', views.customers, name='customers'),


   path('create_order/<str:pk_id>', views.createOrders, name='create_order'),
   path('update_order/<str:pk_id>/', views.updateOrder, name='update_order'),
   path('delete_order/<str:pk_id>/', views.deleteOrder, name='delete_order')

]
 