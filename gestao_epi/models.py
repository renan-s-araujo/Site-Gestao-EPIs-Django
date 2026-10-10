from django.db import models


class Colaborador(models.Model):
    SETORES = [
        ('Manutenção', 'Manutenção'),
        ('Produção', 'Produção'),
        ('Expedição', 'Expedição'),
        ('Qualidade', 'Qualidade'),
        ('Administrativo', 'Administrativo'),
    ]

    STATUS = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]


    matricula = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    cargo = models.CharField(max_length=100)  # Texto livre digitado pelo usuário
    setor = models.CharField(max_length=50, choices=SETORES)


    status = models.CharField(max_length=10, choices=STATUS, default='Ativo')
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.matricula} - {self.nome} ({self.cargo})'

    class Meta:
        ordering = ['nome']
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'