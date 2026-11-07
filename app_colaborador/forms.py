from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Colaborador, Equipamento, Emprestimo


class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', max_length=254)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'DIgite seu nome de usuário',
            'email': 'voce@empresa.com.br',
            'password1': 'Crie uma senha segura',
            'password2': 'Digite a senha novamente',
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders[name],
                'autocomplete': 'new-password' if name.startswith('password') else name,
                'aria-describedby': f'{name}-ajuda {name}-erros',
            })
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['username'].label = 'Usuário'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar senha'
        self.fields['username'].help_text = 'Até 150 caracteres. Use letras, números ou @/./+/-/_.'
        self.fields['password1'].help_text = 'Use pelo menos 8 caracteres. Evite dados pessoais, senhas comuns ou apenas números.'
        self.fields['password2'].help_text = ''

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

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = [
            'ca',
            'nome',
            'tipo',
            'status',
            'quantidade_disponivel'
        ]

        widgets = {
            'ca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o CA do equipamento'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do equipamento'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quantidade_disponivel': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }



class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = [
            'colaborador',
            'equipamento',
            'data_prevista_devolucao',
            'status',
        ]

        widgets = {
            'colaborador': forms.Select(attrs={
                'class': 'form-control'
            }),
            'equipamento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_prevista_devolucao': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['colaborador'].queryset = (
            Colaborador.objects.filter(status='Ativo')
        )

        self.fields['equipamento'].queryset = (
            Equipamento.objects.filter(status='Ativo')
        )

        self.fields['status'].choices = [
            ('Emprestado', 'Emprestado'),
            ('Fornecido', 'Fornecido'),
        ]

        self.fields['data_prevista_devolucao'].required = False

        self.fields['data_prevista_devolucao'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        data_prevista = cleaned_data.get('data_prevista_devolucao')

        if status == 'Emprestado':
            if not data_prevista:
                self.add_error(
                    'data_prevista_devolucao',
                    'Informe a data prevista para devolução.'
                )
            elif data_prevista <= timezone.now():
                self.add_error(
                    'data_prevista_devolucao',
                    'A data prevista deve ser futura.'
                )

        elif status == 'Fornecido':
            cleaned_data['data_prevista_devolucao'] = None

        return cleaned_data


class AtualizarEmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = [
            'status',
            'data_devolucao',
            'observacao_devolucao',
        ]

        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_devolucao': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'observacao_devolucao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre a devolução'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['data_devolucao'].required = False
        self.fields['observacao_devolucao'].required = False

        self.fields['data_devolucao'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        data_devolucao = cleaned_data.get('data_devolucao')

        if status in ['Devolvido', 'Danificado', 'Perdido']:
            if not data_devolucao:
                self.add_error(
                    'data_devolucao',
                    'Informe a data da devolução ou ocorrência.'
                )
            elif data_devolucao > timezone.now():
                self.add_error(
                    'data_devolucao',
                    'A data não pode estar no futuro.'
                )
        else:
            cleaned_data['data_devolucao'] = None
            cleaned_data['observacao_devolucao'] = ''

        return cleaned_data
