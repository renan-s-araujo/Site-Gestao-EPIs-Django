from django import forms
from .models import Colaborador


class ColaboradorForm(forms.ModelForm):

    class Meta:

        model = Colaborador
        fields = ['nome', 'cargo', 'setor']  # Apenas os campos do modal
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o nome completo',
                    'required': 'required',
                }
            ),
            'cargo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Técnico de Manutenção, TST, etc.',
                    'required': 'required',
                }
            ),
            'setor': forms.Select(
                attrs={'class': 'form-control', 'required': 'required'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['setor'].choices = [
            ('', 'Selecione o setor')
        ] + list(Colaborador.SETORES)