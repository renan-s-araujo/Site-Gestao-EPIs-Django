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


class Equipamento(models.Model):
    TIPOS =[
        ("Óculos", "Óculos"),
        ("Capacete", "Capacete"),
        ("Protetor auricular", "Protetor auricular"),
        ("Máscara", "Máscara"),
    ]

    STATUS = [
        ("Ativo", "Ativo"),
        ("Inativo", "Inativo"),
    ]

    ca = models.CharField(primary_key=True)
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=150, choices=TIPOS)
    status = models.CharField(max_length=10, choices=STATUS, default='Ativo')
    quantidade_disponivel = models.PositiveIntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ca} - {self.nome}"

    class Meta:
        ordering = ["nome"]
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"



class Emprestimo(models.Model):

    STATUS = [
        ('Emprestado', 'Emprestado'),
        ('Fornecido', 'Fornecido'),
        ('Devolvido', 'Devolvido'),
        ('Danificado', 'Danificado'),
        ('Perdido', 'Perdido'),
    ]

    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )

    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )

    data_emprestimo = models.DateTimeField(
        auto_now_add=True
    )

    data_prevista_devolucao = models.DateTimeField(
        null=True,
        blank=True
    )

    data_devolucao = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS,
        default='Emprestado'
    )

    observacao_devolucao = models.TextField(
        blank=True,
        default=''
    )

    def __str__(self):
        return (
            f'{self.colaborador.nome} - '
            f'{self.equipamento.nome} - '
            f'{self.status}'
        )

    class Meta:
        ordering = ['-data_emprestimo']
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
