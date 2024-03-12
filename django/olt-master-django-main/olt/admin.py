from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import Perfil

# Register your models here.

class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'setor']  # Defina os campos que você deseja visualizar na lista
    search_fields = ['user__username', 'setor']  # Campos que você quer poder pesquisar

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

# Estende a visualização padrão do User para incluir o Perfil inline
class UserAdmin(DefaultUserAdmin):
    inlines = (PerfilInline, )

admin.site.register(Perfil, PerfilAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)