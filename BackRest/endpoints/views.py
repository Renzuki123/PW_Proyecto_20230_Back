from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import Categoria, Platos
from django.http import JsonResponse

@csrf_exempt
def ObtenerCategoria(request):
    if request.method == 'GET':
        categorias = Categoria.objects.raw(raw_query='SELECT "id"AS ID, category, dish FROM public."Categoria" order by id;')
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


def cambiarEstado_Pedido(request):
    if request.method == 'POST':
        # Obtener el id y el nuevo estado del pedido desde la solicitud POST
        pedido_id = request.POST.get('id')
        nuevo_estado = request.POST.get('estado')

        # Actualizar el estado del pedido en la base de datos
        pedidos = [
            {
                'id': 1,
                'alimento': 'Hamburguesa',
                'precio': 100,
                'fecha': '2023-02-09',
                'hora': '13:00',
                'estado': 'pendiente',
            },
            {
                'id': 2,
                'alimento': 'Pizza',
                'precio': 150,
                'fecha': '2023-02-09',
                'hora': '14:00',
                'estado': 'pendiente',
                },
                {
                'id': 3,
                'alimento': 'Ensalada',
                'precio': 80,
                'fecha': '2023-02-09',
                'hora': '15:00',
                'estado': 'pendiente',
                },
                {
                'id': 4,
                'alimento': 'Sushi',
                'precio': 200,
                'fecha': '2023-02-09',
                'hora': '16:00',
                'estado': 'pendiente',
                },
                {
                'id': 5,
                'alimento': 'Parrillada',
                'precio': 250,
                'fecha': '2023-02-09',
                'hora': '17:00',
                'estado': 'pendiente',
                },
                {
                'id': 6,
                'alimento': 'Pasta',
                'precio': 120,
                'fecha': '2023-02-09',
                'hora': '18:00',
                'estado': 'pendiente',
                },
                {
                'id': 7,
                'alimento': 'Tacos',
                'precio': 90,
                'fecha': '2023-02-09',
                'hora': '19:00',
                'estado': 'pendiente',
                },
                {
                'id': 8,
                'alimento': 'Sopa',
                'precio': 70,
                'fecha': '2023-02-09',
                'hora': '20:00',
                'estado': 'pendiente',
                },
                {
                'id': 9,
                'alimento': 'Churrasco',
                'precio': 180,
                'fecha': '2023-02-09',
                'hora': '21:00',
                'estado': 'pendiente',
                },
                {
                'id': 10,
                'alimento': 'Empanadas',
                'precio': 60,
                'fecha': '2023-02-09',
                'hora': '22:00',
                'estado': 'pendiente',
                }
            
        ]
        for pedido in pedidos:
            if pedido['id'] == int(pedido_id):
                pedido['estado'] = nuevo_estado

        # Acá lo que se hace es devolver una respuesta JSON con el nuevo estado del pedido actualizado
        return JsonResponse({'id': pedido_id, 'estado': nuevo_estado})