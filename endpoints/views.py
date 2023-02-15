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


# Create your views here.
# Ruta: /hola
def holaEndpoint(request):
    # Logica de respuesta ante HTTP request
    return HttpResponse("HOLA!!!")

# Ruta: /adios
def endpoint2(request):
    return HttpResponse("ADIOS!!!")

# Ruta: 
def htmlEndpoint(request):
    return HttpResponse("""
    <html>
        <body>
            <h1>Programación web</h1>
            <img src = "" />
        </body>
    </html>
    """)

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

        if idCategoria == "-1" :
            peliculasQS = Pelicula.objects.all()
        else:
            peliculasQS = Pelicula.objects.filter(categoria__pk=idCategoria)
        
        for p in peliculasQS:
            peliculasFiltradas.append({
                "id" : p.pk,
                "nombre" : p.nombre,
                "url" : p.url,
                "categoria" : {
                    "id" : p.categoria.pk,
                    "nombre" : p.categoria.nombre
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
        {"id" : 1, "imagen" : "https://supervalu.ie/thumbnail/1440x480/var/files/real-food/recipes/Uploaded-2020/spaghetti-bolognese-recipe.jpg", "texto" : "Ricos fideos a la italiana"},
        {"id" : 2, "imagen" : "https://placeralplato.com/files/2015/06/pizza-Margarita.jpg", "texto" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        {"id" : 3, "imagen" : "https://i.imgur.com/xYQlyoY.png", "texto" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        {"id" : 4, "imagen" : "https://i.imgur.com/jxtsRAc.png", "texto" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
    ]
    dictResponse = {
        "error" : "",
        "recomendaciones" : recomendaciones
    }
    strResponse = json.dumps(dictResponse)
    return HttpResponse(strResponse)

@csrf_exempt
def verEstado(request):
    pedidos = [
        { "id": 1, "nombre": "Renzo", "plato": "fideos", "direccion": "Pueblo Libre", "estado": "en preparación", "codigo": "ABC123" },
        { "id": 2, "nombre": "Juan", "plato": "pizza", "direccion": "Jesus Maria", "estado": "en preparación", "codigo": "DEF456" },
        { "id": 3, "nombre": "Roberto", "plato": "ensalada", "direccion": "Los Olivos", "estado": "en preparación", "codigo": "GHI789" }
    ]

    if request.method == "GET":
        dictResponse = {
            "error" : "",
            "arreglo" : pedidos
        }
        return HttpResponse(json.dumps(dictResponse))
    else:
        return HttpResponse("Tipo de petición incorrecto, por favor usar GET")