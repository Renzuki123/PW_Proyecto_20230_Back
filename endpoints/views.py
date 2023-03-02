from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
import json
from endpoints.models import User, Plato, Restaurante, Pedido, PedidoXPlato
from .models import Categoria, Platos # SOLIMANO

# Create your views here.
# Si la peticion es GET: se puede enviar por: 1) Path parameter 2) Query Parameter. La desventaja está en que la data se envía mediante el url (inseguro)

@csrf_exempt
def ObtenerRecomendaciones(request):
    recomendaciones = []
    for plato in Plato.objects.all():
        recomendacion = {
            "id": plato.id,
            "imagen": plato.img,
            "descripcion": plato.descripcion,
        }
        recomendaciones.append(recomendacion)

    dictResponse = {
        "error": "",
        "recomendaciones": recomendaciones
    }
    strResponse = json.dumps(dictResponse)
    return HttpResponse(strResponse)

"""
@csrf_exempt
def ObtenerPlatosGenericos(request):
    if request.method == 'GET':
        Platos = [
            {
                'id': 1,
                'image':
                'https://supervalu.ie/thumbnail/1440x480/var/files/real-food/recipes/Uploaded-2020/spaghetti-bolognese-recipe.jpg',
                'name': 'Spaghetti Bolognese',
                'price': 10,
            },

            {
                'id': 2,
                'image':
                'https://placeralplato.com/files/2015/06/pizza-Margarita.jpg',
                'name': 'Pizza Margherita',
                'price': 12,
            },

            {
                'id': 3,
                'image':
                'https://www.diariamenteali.com/medias/receta-lasgnable-lasagna-de-carne-1900Wx500H?context=bWFzdGVyfGltYWdlc3w0NDg2NzY2fGltYWdlL3BuZ3xoMTgvaGVkLzkyNjA1NzI2MzkyNjIvcmVjZXRhLWxhc2duYWJsZS1sYXNhZ25hLWRlLWNhcm5lXzE5MDBXeDUwMEh8YzQyNDA3YWE1Nzc4YWZlY2YwYTBhZjkwOGFhMzhmYmMxMzQ3NTY2NDlkMmYxZDQ4NWMzNGY4Njk5YzY2OGFkMQ',
                'name': 'Lasagna',
                'price': 15,
            },

            {
                'id': 4,
                'image':
                'https://assets.tmecosys.com/image/upload/t_web600x528/img/recipe/ras/Assets/b89f8de9-0f93-4976-b318-9ab04db353bc/Derivates/d3a08a3c-abb2-452e-9121-168f67c992c8.jpg',
                'name': 'Cesar salad',
                'price': 10,
            },
        ]
        data = {'platos_genericos': Platos}
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        carrito = json.loads(request.body)
        total = obtener_total(carrito)
        return JsonResponse({'total': total})
    
    dictResponse = {
            "error": "",
            "platos_genericos": Platos
        }
    strResponse = json.dumps(dictResponse)
    return HttpResponse(strResponse)
"""

@csrf_exempt
def ObtenerPlatosGenericos(request):
    if request.method == 'GET':
        platos = Plato.objects.all()
        platos_list = [{'id': plato.id, 'imagen': plato.img, 'name': plato.nombre, 'precio': plato.precio} for plato in platos]
        data = {'platos_genericos': platos_list}
        return JsonResponse(data, safe=False)
    
    dictResponse = {
            "error": "",
            "platos_genericos": platos_list
        }
    strResponse = json.dumps(dictResponse)
    return HttpResponse(strResponse)

@require_POST
@csrf_exempt
def registrar_pedido(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(request.body)
        nombre = data['nombre']
        total = data['total']
        direccion = data['direccion']
        referencias = data['referencias']
        detalles = data['detalles']
        metodo = data['metodo']
        pedido = Pedido(nombre=nombre, total=total, direccion=direccion, referencias=referencias, detalles=detalles, metodo=metodo, estado="S")
        #pedido = Pedido(nombre=nombre, total=total, direccion=direccion, referencias=referencias, detalles=detalles, metodo=metodo)
        pedido.save()

        detalles = json.loads(detalles)
        detalles_pedido = []
        
        for item in detalles:
            plato = Plato.objects.get(id=item['id']) 
            cantidad = int(item['cantidad'])
            detalles_pedido.append({'nombre': plato.nombre, 'cantidad': cantidad})
            pedido_x_plato = PedidoXPlato(pedido=pedido, plato=plato, cantidad=cantidad)
            pedido_x_plato.save()
        
        return JsonResponse({'success': True})
        
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def pedidos(request):
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        pedidos_list = []
        for pedido in pedidos:
            pedido_dict = {
                'id': pedido.id,
                'nombre': pedido.nombre,
                'detalles': pedido.detalles,
                'direccion': pedido.direccion,
                'metodo': pedido.metodo,
                'codigo': pedido.codigo,
                'total': pedido.total,
                'estado': pedido.estado
            }
            pedidos_list.append(pedido_dict)
        return JsonResponse({'pedidos': pedidos_list})

@require_POST
@csrf_exempt
def buscar_pedido_por_codigo(request):
    if request.method == 'GET':
        codigo_pedido = request.GET.get('codigo_pedido', '')
        pedidos = Pedido.objects.filter(codigo=codigo_pedido)
        pedidos_list = []
        for pedido in pedidos:
            pedido_dict = {
                'id': pedido.id,
                'nombre': pedido.nombre,
                'detalles': pedido.detalles,
                'direccion': pedido.direccion,
                'metodo': pedido.metodo,
                'codigo': pedido.codigo,
                'total': pedido.total,
                'estado': pedido.estado
            }
            pedidos_list.append(pedido_dict)
        return JsonResponse({'pedidos': pedidos_list})

@csrf_exempt
@require_POST
def cambiarEstado_Pedido(request):
    if request.method == 'POST':
        # Obtener el id y el nuevo estado del pedido desde la solicitud POST
        data = json.loads(request.body)
        pedido_id = data.get('id')
        nuevo_estado = data.get('estado')
        # Verificar si existe un pedido con el id proporcionado
        if Pedido.objects.filter(id=pedido_id).exists():
            # Actualizar el estado del pedido en la base de datos
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.estado = nuevo_estado
            pedido.save()

            # Devolver una respuesta JSON con el nuevo estado del pedido actualizado
            return JsonResponse({'id': pedido_id, 'estado': nuevo_estado})
        else:
            # Devolver una respuesta JSON con un mensaje de error si no se encontró el pedido
            return JsonResponse({'error': f'Pedido con id {pedido_id} no encontrado'})
    
"""
@csrf_exempt
def ObtenerRecomendaciones(request):

    recomendaciones = [
        {"id": 1, "imagen": "https://supervalu.ie/thumbnail/1440x480/var/files/real-food/recipes/Uploaded-2020/spaghetti-bolognese-recipe.jpg",
            "texto": "Ricos fideos a la italiana"},
        {"id": 2, "imagen": "https://placeralplato.com/files/2015/06/pizza-Margarita.jpg",
            "texto": "Pizza italiana 10/10, no te la puedes perder"},
        {"id": 3, "imagen": "https://www.recetasdesbieta.com/wp-content/uploads/2018/10/lasagna-original..jpg",
            "texto": "Lasagna italiana, tu vida no será la misma luego de probarla"},
        {"id": 4, "imagen": "https://assets.tmecosys.com/'image'/upload/t_web600x528/img/recipe/ras/Assets/b89f8de9-0f93-4976-b318-9ab04db353bc/Derivates/d3a08a3c-abb2-452e-9121-168f67c992c8.jpg",
            "texto": "Cesar salad, luego de probarla tu mente quedará volando"},
    ]
    dictResponse = {
        "error": "",
        "recomendaciones": recomendaciones
    }
    strResponse = json.dumps(dictResponse)
    return HttpResponse(strResponse)
""" 

@csrf_exempt
def verEstado(request):
    pedidos = [
        {"id": 1, "nombre": "Renzo", "restaurante": "Pizzeria Artesanal", "plato": "fideos",
            "direccion": "Pueblo Libre", "estado": "en preparación", "codigo": "ABC123"},
        {"id": 2, "nombre": "Renzo", "restaurante": "Pizzeria Artesanal", "plato": "pizza",
            "direccion": "Pueblo Libre", "estado": "en preparación", "codigo": "DEF456"},
        {"id": 3, "nombre": "Renzo", "restaurante": "Bembos", "plato": "ensalada",
            "direccion": "Pueblo Libre", "estado": "en preparación", "codigo": "GHI789"}
    ]

    if request.method == "GET":
        dictResponse = {
            "error": "",
            "arreglo": pedidos
        }
        return HttpResponse(json.dumps(dictResponse))
    else:
        return HttpResponse("Tipo de petición incorrecto, por favor usar GET")


@csrf_exempt
def registrarentrega(request):
    if request.method == "POST":
        dictCode = json.loads(request.body)
        code = dictCode["code"]
        error = "No se encontró ese pedido"
        if code != None:
            try:
                pedido = Pedido.objects.get(codigo=code)
                producto = {"id": pedido.id, "nombre": pedido.nombre,"detalles": pedido.detalles, "direccion": pedido.direccion, "metodo": pedido.metodo,"codigo": pedido.codigo, "estado": pedido.estado, "total": str(pedido.total)}
                dictOK = {
                    "error": "",
                    "producto": producto
                }
                strOK = json.dumps(dictOK)
                return HttpResponse(strOK)
            except Pedido.DoesNotExist:
                pass
        else:
            error = "Por favor envíe un código de pedido"
        dictError = {
            "error": error
        }
        return HttpResponse(json.dumps(dictError))
    else:
        return HttpResponse("Tipo de petición incorrecto, por favor usar POST")

# Endpoints de Solimano
@csrf_exempt
def ObtenerCategoria(request):
    if request.method == 'GET':
        categorias = Categoria.objects.raw(raw_query='SELECT "id"AS ID, category, dish FROM endpoints_categoria order by id;')
        categoria_list = [{'id': categoria.id, 'category': categoria.category, 'dish': categoria.dish} for categoria in categorias]
        data = {'categorias' : categoria_list}
        return JsonResponse(data, safe = False)

@csrf_exempt        
def LoginRest(request):
    if request.method == "POST":

        dictDataRequest = json.loads(request.body)

        usuario = dictDataRequest["usuario"]

        password = dictDataRequest["password"]

        if usuario == "pedro" and password == "pedro2023":
            # Correcto
            dictOk = {
                "error": ""
            }
            return HttpResponse(json.dumps(dictOk))
        else:
            # Error login
            dictError = {
                "error": "Error en login"
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)

    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

@csrf_exempt  
def CategPedidos(request):
    if request.method != "GET":
        dictError = {
            "error": "Tipo de peticion no existe."
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    else: 
        lista = [
            {
            "id": 1,
            "category": "Italiana",
            "Dish": "Spaghetti Carbonara"
            },
            {
            "id": 2,
            "category": "Mexicana",
            "Dish": "Tacos al Pastor"
            },
            {
            "id": 3,
            "category": "Japonesa",
            "Dish": "Sushi de salmón"
            },
            {
            "id": 4,
            "category": "India",
            "Dish": "Pollo Tikka Masala"
            },
            {
            "id": 5,
            "category": "Americana",
            "Dish": "Hamburguesa con queso"
            },
            {
            "id": 6,
            "category": "Mediterránea",
            "Dish": "Ensalada griega"
            },
            {
            "id": 7,
            "category": "China",
            "Dish": "Arroz frito"
            },
            {
            "id": 8,
            "category": "Francesa",
            "Dish": "Croissants"
            },
            {
            "id": 9,
            "category": "Coreana",
            "Dish": "Bibimbap"
            },
            {
            "id": 10,
            "category": "Venezolana",
            "Dish": "Arepa de Reina Pepiada"
            },
            {
            "id": 11,
            "category": "Hamburguesas",
            "Dish": "Hamburguesa de pollo"
            },
            {
            "id": 12,
            "category": "Pastas",
            "Dish": "Fettuccine Alfredo"
            },
            {
            "id": 13,
            "category": "Postres",
            "Dish": "Pastel de zanahoria"
            },
            {
            "id": 14,
            "category": "Comida rápida",
            "Dish": "Tacos de pescado"
            },
            {
            "id": 15,
            "category": "Comida vegetariana",
            "Dish": "Ensalada de garbanzos"
            },
            {
            "id": 16,
            "category": "Parrilladas",
            "Dish": "Asado de tira"
            },
            {
            "id": 17,
            "category": "Comida mexicana",
            "Dish": "Chiles en nogada"
            },
            {
            "id": 18,
            "category": "Comida italiana",
            "Dish": "Spaghetti carbonara"
            },
            {
            "id": 19,
            "category": "Sopas",
            "Dish": "Sopa de cebolla"
            },
            {
            "id": 20,
            "category": "Comida china",
            "Dish": "Pollo kung pao"
            }
        ]

        dictResponse = {
            "error":"",
            "pedido": lista
        }
        strResponse = json.dumps(dictResponse["pedido"])
        return HttpResponse(strResponse)

@csrf_exempt  
def Actualizar_Pedido(request):
   
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    dictCategoria = json.loads(request.body)

    identificador = dictCategoria["id"]
    cat = Categoria.objects.get(pk=identificador) # Obtenemos cat de bd

    if dictCategoria.get("nombre") != None:
        cat.nombre = dictCategoria.get("nombre")

    if dictCategoria.get("estado") != None:
        cat.estado = dictCategoria.get("estado")

    cat.save() # Se modifica la bd

    dictOK = {
        "error" : ""
    }
    return HttpResponse(json.dumps(dictOK))

@csrf_exempt  
def Verificar_EstadoPedido(request):
    if request.method != "GET":
        dictError = {
            "error": "Tipo de peticion no existe."
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    else: 
        lista = [
            {
                "id": 1,
                "cod":12345,
                "producto" : "Pizza Americana",
                "cliente": "Miley Cyrus",
                "hora": "1 pm"
            },
            {
                "id": 2,
                "cod":12346,
                "producto" : "Pizza Suprema",
                "cliente": "Alan Garcia",
                "hora": "2 pm"
            },
            {
                "id": 3,
                "cod":12349,
                "producto" : "Pizza Hawaiana",
                "cliente": "Renzo Cavero",
                "hora": "3 pm"
            }]
        

        dictResponse = {
            "error":"",
            "pedido": lista
        }
        strResponse = json.dumps(dictResponse["pedido"])
        return HttpResponse(strResponse)

# Endpoints Renzo Cavero:
# /endpoints/login


@csrf_exempt
def login(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=usuario, password=password)

        if user is not None:
            # Log user in
            login(request, user)
            # Redirect to /req2
            return redirect('/req2')
        else:
            dictError = {
                "error": "INICIO DE SESIÓN FALLIDO"
            }
            return JsonResponse(dictError)
    else:
        dictError = {
            "error": "SOLICITUD NO ES DE TIPO POST"
        }
        return JsonResponse(dictError)


def obtenerPlatos(request):
    if request.method == "GET":
        idCat = request.GET.get("Restaurante")

        if idCat == None:
            dictError = {
                "error": "Enviar categoria."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)

        platosFiltr = []

        if idCat == "-1":
            platosQS = Plato.objects.all()
        else:
            platosQS = Plato.objects.filter(categoria__pk=idCat)

        for i in platosQS:
            platosFiltr.append({
                "id": i.pk,
                "'title'": i.nombre,
                "price": float(i.precio),
                "img": i.img,
                "desc": i.descripcion,
                "'category'": i.categoria.nombre
            })

        dictResponse = {
            "error": "",
            "carta": platosFiltr
        }
        strResponse = json.dumps(dictResponse)
        return HttpResponse(strResponse)
    else:
        dictError = {
            "error": "NO EXISTE EL TIPO DE PETICION"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)


@csrf_exempt
def obtenerRestaurante(request):
    if request.method == "GET":
        listaRestaurantesQuerySet = Restaurante.objects.all()
        listaRestaurantes = []
        for r in listaRestaurantesQuerySet:
            listaRestaurantes.append({
                "id": r.pk,
                "url": r.url,
                "title": r.title,
                "category": r.category,
                "description": r.description,
                "date": r.date,
            })

        dictOK = {
            "error": "",
            "data": listaRestaurantes
        }
        #strOK = json.dumps(dictOK["data"])
        return HttpResponse(json.dumps(dictOK))

    else:
        dictError = {
            "error": "NO EXISTE EL TIPO DE PETICION"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
        
