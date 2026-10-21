from django.contrib import admin
from .models import Colaborador

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = (
        'matricula',
        'nome',
        'setor',
        'status',
    )

    search_fields = (
        'matricula',
        'nome',
    )

    list_filter = (
        'setor',
        'status',
    )

    ordering = ('nome',)