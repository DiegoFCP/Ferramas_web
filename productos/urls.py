from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),  # URL para ver la lista de productos
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login_staff/', views.login_staff, name='login_staff'),
    path('cart/', views.cart, name='cart'),
    path('post_compra/', views.post_compra, name='post_compra'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('iniciar_pago/', views.iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago')

]
