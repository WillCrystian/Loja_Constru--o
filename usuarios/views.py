from http.client import HTTPResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from rolepermissions.decorators import has_permission_decorator
from .models import Users
from django.urls import reverse
from django.contrib import auth, messages



@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == 'GET':
        vendedores = Users.objects.filter(cargo = 'V')
        return render(request, 'cadastrar_vendedor.html',{'vendedores': vendedores})
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
        messages.add_message(request, messages.SUCCESS, 'Vendedor cadastrado com sucesso.')
        return redirect(reverse('cadastrar_vendedor'))
    
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

@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario(request, id):
    vendedor = get_object_or_404(Users, id= id)
    vendedor.delete()
    messages.add_message(request, messages.SUCCESS, 'Vendedor excluido com sucesso.')
    return redirect(reverse('cadastrar_vendedor'))
            

    
        
