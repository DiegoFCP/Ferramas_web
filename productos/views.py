import bcchapi
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Producto

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from django.conf import settings

import uuid

from django.http import HttpResponse, JsonResponse

from bcchapi import Siete

from datetime import datetime

from decimal import Decimal, ROUND_DOWN
from django.core.paginator import Paginator

api = Siete("diegocortes.pinilla@gmail.com", "Cuimi199!")

def lista_productos(request):
    query = request.GET.get('search')
    show_all = request.GET.get('show_all')

    if show_all:
        productos = Producto.objects.all()  # Mostrar todos los productos
    elif query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()  # Mostrar todos los productos si no hay búsqueda

    # Añadir paginación (12 productos por página)
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')  # Obtener el número de página actual
    productos_paginados = paginator.get_page(page_number)

    return render(request, 'productos/lista_productos.html', {
        'productos': productos_paginados,
        'query': query
    })
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


def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    cart = request.session.get("cart", [])

    # Verificar si el producto ya está en el carrito y aumentar la cantidad
    for item in cart:
        if item["id_producto"] == producto_id:
            item["cantidad"] += 1
            break
    else:
        # Si no existe, añadir nuevo
        cart.append({
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "precio": float(producto.precio),
            "cantidad": 1
        })

    request.session["cart"] = cart

    # Responder con JSON si es AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Producto añadido al carrito"})

    return redirect("cart")


def cart(request):
    # Obtener el carrito desde la sesión
    cart = request.session.get('cart', [])

    # Calcular el total en CLP y los subtotales
    total_clp = 0
    for item in cart:
        item['subtotal'] = item['cantidad'] * item['precio']
        total_clp += item['subtotal']
    
    # Obtener el tipo de cambio y calcular el total en USD
    tipo_cambio = obtener_tipo_cambio()
    total_usd = total_clp / tipo_cambio if tipo_cambio else None

    # Guardar ambos totales en la sesión
    request.session['cart_total_clp'] = total_clp
    request.session['cart_total_usd'] = int(total_usd) if total_usd else None

    # Pasar los datos al contexto de la plantilla
    return render(request, 'productos/cart.html', {
        'cart': cart,
        'total_clp': total_clp,
        'total_usd': total_usd,
        'tipo_cambio': tipo_cambio,
        'error_message': "No se pudo obtener el tipo de cambio en este momento." if not tipo_cambio else None,
    })

# Aumentar cantidad
def increase_quantity(request, producto_id):
    cart = request.session.get("cart", [])
    for item in cart:
        if item["id_producto"] == producto_id:
            item["cantidad"] += 1
            break
    request.session["cart"] = cart
    return JsonResponse({"success": True, "message": "Cantidad aumentada"})

# Disminuir cantidad
def decrease_quantity(request, producto_id):
    cart = request.session.get("cart", [])
    for item in cart:
        if item["id_producto"] == producto_id:
            if item["cantidad"] > 1:
                item["cantidad"] -= 1
            else:
                cart.remove(item)  # Si es la última unidad, se elimina del carrito
            break
    request.session["cart"] = cart
    return JsonResponse({"success": True, "message": "Cantidad disminuida"})

# Eliminar del carrito
def remove_from_cart(request, producto_id):
    cart = request.session.get("cart", [])
    cart = [item for item in cart if item["id_producto"] != producto_id]
    request.session["cart"] = cart
    return JsonResponse({"success": True, "message": "Producto eliminado del carrito"})


def post_compra(request):
    # Obtener el carrito y el total desde la sesión
    cart = request.session.get('cart', [])
    total = request.session.get('cart_total', 0)

    # Limpiar el carrito de la sesión después de la compra
    request.session['cart'] = []
    request.session['cart_total'] = 0

    # Pasar el carrito y el total al contexto de la plantilla
    return render(request, 'productos/post_compra.html', {
        'cart': cart,
        'total': total,
        'order_number': '123456'  # Genera el número de pedido real si es necesario
    })

def admin_dashboard(request):
    # Esta vista sería la del dashboard del administrador
    return render(request, 'productos/admin_dashboard.html')

from transbank.webpay.webpay_plus.transaction import Transaction


def iniciar_pago(request):
    # Obtiene el parámetro de divisa seleccionado
    divisa = request.GET.get('divisa', 'CLP')
    buy_order = str(uuid.uuid4())[:26]  # Truncamos el UUID a 26 caracteres
    session_id = str(uuid.uuid4())[:26]

    # Obtiene el total del carrito de la sesión en CLP o USD
    if divisa == 'USD':
        amount = request.session.get('cart_total_usd', 0)  # Usar el total en USD desde la sesión
    else:
        amount = request.session.get('cart_total_clp', 0)  # Usar el total en CLP desde la sesión

    # Verifica si el monto es válido
    if amount <= 0:
        return redirect('cart')  # Redirige al carrito si el monto no es válido

    return_url = request.build_absolute_uri(reverse('confirmar_pago'))

    # Llamada a la API de Transbank
    try:
        response = Transaction().create(
            buy_order=buy_order,
            session_id=session_id,
            amount=amount,
            return_url=return_url
        )
    except Exception as e:
        # Maneja el error de Transbank aquí
        print("Error en la transacción:", e)
        return redirect('cart')  # Redirige al carrito en caso de error

    return redirect(response['url'] + '?token_ws=' + response['token'])

def confirmar_pago(request):
    token = request.GET.get("token_ws")
    if token:
        response = Transaction().commit(token)
        return render(request, 'productos/post_compra.html', {'response': response})
    else:
        return render(request, 'productos/error.html', {'error': 'Token no encontrado'})


from bcchapi import Siete

def obtener_tipo_cambio():
    try:
        # Inicializa la conexión con credenciales
        siete = bcchapi.Siete("diegocortes.pinilla@gmail.com", "Cuimi199!")
        
        # Establece la fecha actual
        fecha_actual = datetime.today().strftime('%Y-%m-%d')
        
        # Realiza la consulta del tipo de cambio
        tipo_cambio = siete.cuadro(
            series=["F073.TCO.PRE.Z.D"],
            nombres=["dolar"],
            desde=fecha_actual
        )
        
        # Obtiene el último valor del tipo de cambio
        return tipo_cambio['dolar'].iloc[-1]
    except Exception as e:
        print(f"Error al obtener el tipo de cambio: {e}")
        return None