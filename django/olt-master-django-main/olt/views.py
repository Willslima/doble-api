from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from .models import Usuario
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from .forms import UserRegisterForm, ProfileForm
# Create your views here.

def user_is_noc(user):
    return user.perfil.setor == "NOC"

@login_required
def menu(request):
    return render(request, 'olt/index.html')

@login_required
def cadastro(request):
    return render(request, 'olt/cadastro.html')

@login_required
def provisionamento(request):
    return render(request, 'olt/provisionamento.html')

@login_required
def troca_equipamento(request):
    return render(request, 'olt/troca_equipamento.html')

@login_required
def status(request):
    return render(request, 'olt/status_cliente.html')

@login_required
def sinal(request):
    return render(request, 'olt/verificar_sinal.html')
@login_required
def verificar_caixa(request):
    return render(request, 'olt/verificar_caixa.html')

@login_required
def alterar_dados(request):
    return render(request, 'olt/alterar_dados.html')

@login_required
def excluir(request):
    return render(request, 'olt/excluir_cliente.html')

@login_required
def logs(request):
    return render(request, 'olt/logs.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.setor = 'TECNICO'
            profile.save()

            login(request, user)
            return redirect('verificacao_cadastro')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'cadastro.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def verifica_cadastro(request):
    return render(request, 'olt/verificacao_cadastro.html')