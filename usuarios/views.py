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
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        
        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Sua senha possui menos de 6 letras.')
            return redirect(reverse('cadastrar_vendedor'))

        user = Users.objects.filter(email = email) 
        
       
        
        if user.exists():
            messages.add_message(request, messages.ERROR, 'Este e-mail já está cadastrado.')
            return redirect(reverse('cadastrar_vendedor'))
        
        user = Users.objects.create_user(username = email,
                                         first_name = first_name,
                                         last_name = last_name,
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
            messages.add_message(request, messages.ERROR, 'Usuário inválido.')
            return redirect(reverse('login'))
        
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Usuário logado com sucesso.')
        return redirect(reverse('login'))

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))    

@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario(request, id):
    vendedor = get_object_or_404(Users, id= id)
    vendedor.delete()
    messages.add_message(request, messages.SUCCESS, 'Vendedor excluido com sucesso.')
    return redirect(reverse('cadastrar_vendedor'))
            

    
        
