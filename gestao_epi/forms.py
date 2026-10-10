from django import forms
from .models import Colaborador

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'matricula', 'setor', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo',
                'required': 'required'
            }),
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a matrícula',
                'required': 'required'
            }),
            'setor': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }