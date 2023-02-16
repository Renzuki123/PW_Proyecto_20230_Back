from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
import json
from endpoints.models import User, Platos, Restaurantes, Categoria

# Create your views here.
# Si la peticion es GET: se puede enviar por: 1) Path parameter 2) Query Parameter. La desventaja está en que la data se envía mediante el url (inseguro)

def obtenerRestaurantes(request):
    if request.method == "GET":
        idCategoria = request.GET.get("categoria")

        if idCategoria == None:
            dictError = {
                "error": "Debe enviar una categoria como query paremeter."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)

        peliculasFiltradas = []

        if idCategoria == "-1":
            peliculasQS = Pelicula.objects.all()
        else:
            peliculasQS = Pelicula.objects.filter(categoria__pk=idCategoria)

        for p in peliculasQS:
            peliculasFiltradas.append({
                "id": p.pk,
                "nombre": p.nombre,
                "url": p.url,
                "categoria": {
                    "id": p.categoria.pk,
                    "nombre": p.categoria.nombre
                }
            })

        dictResponse = {
            "error": "",
            "peliculas": peliculasFiltradas
        }
        strResponse = json.dumps(dictResponse)
        return HttpResponse(strResponse)
    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

@csrf_exempt
def ObtenerRecomendaciones(request):
    recomendaciones = [
        {"id": 1, "imagen": "https://supervalu.ie/thumbnail/1440x480/var/files/real-food/recipes/Uploaded-2020/spaghetti-bolognese-recipe.jpg",
            "texto": "Ricos fideos a la italiana"},
        {"id": 2, "imagen": "https://placeralplato.com/files/2015/06/pizza-Margarita.jpg",
            "texto": "Pizza italiana 10/10, no te la puedes perder"},
        {"id": 3, "imagen": "https://www.diariamenteali.com/medias/receta-lasgnable-lasagna-de-carne-1900Wx500H?context=bWFzdGVyfGltYWdlc3w0NDg2NzY2fGltYWdlL3BuZ3xoMTgvaGVkLzkyNjA1NzI2MzkyNjIvcmVjZXRhLWxhc2duYWJsZS1sYXNhZ25hLWRlLWNhcm5lXzE5MDBXeDUwMEh8YzQyNDA3YWE1Nzc4YWZlY2YwYTBhZjkwOGFhMzhmYmMxMzQ3NTY2NDlkMmYxZDQ4NWMzNGY4Njk5YzY2OGFkMQ",
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

@csrf_exempt
def verEstado(request):
    pedidos = [
        {"id": 1, "nombre": "Renzo", "plato": "fideos", "direccion": "Pueblo Libre",
            "estado": "en preparación", "codigo": "ABC123"},
        {"id": 2, "nombre": "Juan", "plato": "pizza", "direccion": "Jesus Maria",
            "estado": "en preparación", "codigo": "DEF456"},
        {"id": 3, "nombre": "Roberto", "plato": "ensalada",
            "direccion": "Los Olivos", "estado": "en preparación", "codigo": "GHI789"}
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
    pedidos = [
        {"code": 123, "desc": "Lomito saltado", "code_v": 123},
        {"code": 777, "desc": "Chilcanito doble", "code_v": 444},
        {"code": 789, "desc": "Tallarines rojos", "code_v": 333},
    ]

    if request.method == "POST":
        dictCode = json.loads(request.body)
        code = dictCode["code"]
        error = "No se encontró ese pedido"
        if code != None:
            for pedido in pedidos:
                if int(code) == pedido["code"]:
                    dictOK = {
                        "error": "",
                        "producto": pedido
                    }
                    strOK = json.dumps(dictOK)
                    return HttpResponse(strOK)
        else:
            error = "Por favor envíe un código de pedido"
        dictError = {
            "error": error
        }
        return HttpResponse(json.dumps(dictError))
    else:
        return HttpResponse("Tipo de petición incorrecto, por favor usar POST")

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
        idCat = request.GET.get("categoria")

        if idCat == None:
            dictError = {
                "error": "Enviar categoria."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)

        platosFiltr = []

        if idCat == "-1":
            platosQS = Platos.objects.all()
        else:
            platosQS = Platos.objects.filter(categoria__pk=idCat)

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
def obtenerCategorias(request):
    if request.method == "GET":
        listaCategoriasQuerySet = Categoria.objects.all()
        listaCategorias = []
        for c in listaCategoriasQuerySet:
            listaCategorias.append({
                "id": c.id,
                "nombre": c.nombre
            })
        dictOK = {
            "error": " ",
            "categorias": listaCategorias
        }
        return HttpResponse(json.dumps(dictOK))

    else:
        dictError = {
            "error": "NO EXISTE EL TIPO DE PETICION"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

@csrf_exempt
def ObtenerRestaurantesRC(request):
    Restaurantes = [
    {
		'id': 12,
		'image':
			'https://cdn.pixabay.com/photo/2017/12/10/14/47/pizza-3010062_960_720.jpg',
		'title': 'Pizzeria Artesanal 2',
		'category': 'Pizzas',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

	{
		'id': 1,
		'image':
			'https://media.istockphoto.com/id/1342192946/es/foto/filete-de-pollo-a-la-plancha-con-hierbas-aisladas-sobre-fondo-blanco.jpg?s=1024x1024&w=is&k=20&c=nKNA5zbi9_alxW7dpwIGzHeXAbzeOoQdKOS-nGwoKlk=',
		'title': 'Pardos Chicken',
		'category': 'Polleria',
		'description': 'Esto es parte del backend',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Recomendado',
	},

	{
		'id': 2,
		'image':
			'https://media.istockphoto.com/id/1342192946/es/foto/filete-de-pollo-a-la-plancha-con-hierbas-aisladas-sobre-fondo-blanco.jpg?s=1024x1024&w=is&k=20&c=nKNA5zbi9_alxW7dpwIGzHeXAbzeOoQdKOS-nGwoKlk=',
		'title': 'Polleria de Pepe',
		'category': 'Polleria',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'No Recomendado',
	},

    {
		'id': 3,
		'image':
			'https://media.istockphoto.com/id/1425176257/es/foto/salteado-fideos-de-frijoles-con-filete-de-pollo-frito-y-br%C3%B3coli.jpg?s=1024x1024&w=is&k=20&c=NTlOw7Fb_SnBxYYEWuqMxBK4-xV8gUnGuwQ6k81h2Kk=',
		'title': 'Restaurante Asiatico 1',
		'category': 'Asiatica',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Recomendado',
	},

    {
		'id': 4,
		'image':
			'https://media.istockphoto.com/id/1425176257/es/foto/salteado-fideos-de-frijoles-con-filete-de-pollo-frito-y-br%C3%B3coli.jpg?s=1024x1024&w=is&k=20&c=NTlOw7Fb_SnBxYYEWuqMxBK4-xV8gUnGuwQ6k81h2Kk=',
		'title': 'Chifa Jockey',
		'category': 'Asiatica',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

    {
		'id': 5,
		'image':
			'https://cdn.pixabay.com/photo/2016/03/05/19/02/hamburger-1238246_1280.jpg',
		'title': 'MC Donalds',
		'category': 'Hamburguesas',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

    {
		'id': 6,
		'image':
			'https://cdn.pixabay.com/photo/2016/03/05/19/02/hamburger-1238246_1280.jpg',
		'title': 'Bembos',
		'category': 'Hamburguesas',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

    {
		'id': 7,
		'image':
			'https://cdn.pixabay.com/photo/2017/12/10/14/47/pizza-3010062_960_720.jpg',
		'title': 'Pizzeria Artesanal 1',
		'category': 'Pizzas',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

    {
		'id': 8,
		'image':
			'https://cdn.pixabay.com/photo/2017/12/10/14/47/pizza-3010062_960_720.jpg',
		'title': 'Pizzeria Artesanal 2',
		'category': 'Pizzas',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},
    {
		'id': 9,
		'image':
			'https://cdn.pixabay.com/photo/2017/12/10/14/47/pizza-3010062_960_720.jpg',
		'title': 'Pizzeria Artesanal 3',
		'category': 'Pizzas',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

    {
		'id': 10,
		'image':
			'https://cdn.pixabay.com/photo/2021/07/17/01/06/ceviche-6472044_960_720.jpg',
		'title': 'Cevicheria 01',
		'category': 'Pescados Y Mariscos',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

    {
		'id': 11,
		'image':
			'https://cdn.pixabay.com/photo/2021/07/17/01/06/ceviche-6472044_960_720.jpg',
		'title': 'Cevicheria 02',
		'category': 'Pescados Y Mariscos',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

    {
		'id': 13,
		'image':
			'https://cdn.pixabay.com/photo/2016/12/29/15/22/chocolate-1938702_960_720.jpg',
		'title': 'Reposteria de Pepe',
		'category': 'Navideña',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},

    {
		'id': 14,
		'image':
			'https://cdn.pixabay.com/photo/2016/12/29/15/22/chocolate-1938702_960_720.jpg',
		'title': 'Reposteria de Lucho',
		'category': 'Navideña',
		'description':
			'Este es contendio del archivo data.js, aca tienes que ingresar la descrpción - RC',
		'date': 'Publicado el 02 de febrero de 2023',
		'Puntuacion': 'Excelente',
	},  
]
    dictResponse = {
        "error": "",
        "resatuarntes": Restaurantes
    }
    strResponse = json.dumps(dictResponse)
    return HttpResponse(strResponse)
