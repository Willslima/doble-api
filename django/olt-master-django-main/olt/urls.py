from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path("menu/", views.menu, name='menu'),
    path("cadastro/", views.register, name='cadastro'),
    path("provisionamento/", views.provisionamento, name='provisionamento'),
    path("troca-equipamento/", views.troca_equipamento, name='troca-equipamento'),
    path("status/", views.status, name='status'),
    path("verificar-caixa/", views.verificar_caixa, name='verificar_caixa'),
    path("sinal/", views.sinal, name='sinal'),
    path("alterar-dados/", views.alterar_dados, name='alterar_dados'),
    path("excluir/", views.excluir, name='excluir'),
    path("logout/", views.user_logout, name='logout'),
    path("verificacao-cadastro/", views.verifica_cadastro, name='verificacao_cadastro'),
    path("logs-admin/", views.logs, name='logs-admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)