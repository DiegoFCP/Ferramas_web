from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Producto

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from django.shortcuts import render, redirect
from django.conf import settings

import uuid

from django.http import HttpResponse





def lista_productos(request):
    query = request.GET.get('search')
    show_all = request.GET.get('show_all')

    if show_all:
        productos = Producto.objects.all()  # Mostrar todos los productos
    elif query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = []  # Lista vacía cuando no se ha hecho una búsqueda

    return render(request, 'productos/lista_productos.html', {'productos': productos, 'query': query})

def index(request):
    # Página principal
    return render(request, 'productos/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Simulación de autenticación de cliente
        if username == 'cliente' and password == '1234':  # Datos ficticios
            return redirect('cart')  # Redirige a la página del carrito
        else:
            return render(request, 'productos/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'productos/login.html')

def login_staff(request):
    # Login de staff
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Sin validación real, solo una simulación de inicio de sesión
        if username == 'admin' and password == '1234':  # Datos simulados
            return redirect('admin_dashboard')  # Redirige a la página principal si las credenciales son válidas
        else:
            return render(request, 'productos/login_staff.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'productos/login_staff.html')

def cart(request):
    # Página principal
    return render(request, 'productos/cart.html')

def post_compra(request):
    # Página principal
    return render(request, 'productos/post_compra.html')

def admin_dashboard(request):
    # Esta vista sería la del dashboard del administrador
    return render(request, 'productos/admin_dashboard.html')

from transbank.webpay.webpay_plus.transaction import Transaction

def iniciar_pago(request):
    buy_order = "orden12345"
    session_id = "sesion12345"
    amount = 95000
    return_url = request.build_absolute_uri(reverse('confirmar_pago'))

    # Llamada correcta a Transaction.create()
    response = Transaction().create(
        buy_order=buy_order,
        session_id=session_id,
        amount=amount,
        return_url=return_url
    )

    # Redirige al usuario a la URL de pago proporcionada por Transbank
    return redirect(response['url'] + '?token_ws=' + response['token'])


def confirmar_pago(request):
    # Obtiene el token desde la URL (parámetro 'token_ws')
    token = request.GET.get("token_ws")
    
    if token:
        # Llamada correcta a Transaction.commit(token)
        response = Transaction().commit(token)
        
        # Muestra la página de confirmación usando post_compra.html
        return render(request, 'productos/post_compra.html', {'response': response})
    else:
        # Muestra la página de error si el token no está presente
        return render(request, 'productos/error.html', {'error': 'Token no encontrado'})