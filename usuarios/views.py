from http.client import HTTPResponse
from django.shortcuts import render, HttpResponse, redirect
from rolepermissions.decorators import has_permission_decorator
from .models import Users
from django.urls import reverse
from django.contrib import auth


@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_vendedor.html',{})
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = Users.objects.filter(email = email)
        
        if user.exists():
            # TODO: fazer messagens do django
            return HttpResponse('Usuário já existe')
        
        user = Users.objects.create_user(username = email,
                                         email = email,
                                         password = password,
                                         cargo = "V")
        # TODO: redirecionar com uma mensagem
        return HttpResponse('Conta Criada com sucesso')
    
def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('plataform'))
        else:
            return render(request, 'login.html',{})
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(username = email, password = password)
        
        if not user:
            #TODO: retornar com mensagem 
            return HttpResponse('Usuário invalido')
        
        auth.login(request, user)
        
        return HttpResponse('Usuário logado com sucesso')

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))        
            

    
        
