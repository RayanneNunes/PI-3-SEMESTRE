from django.db import models
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User



class Usuario(models.Model):

    id_usuario = models.IntegerField(
        max_length = 10,
        verbose_name = "ID Usuario",
    )
    
    nome = models.CharField(
        max_length = 200,
        verbose_name = "Nome de Usuario",
        help_text = "Digite aqui o nome..."
    )

    email = models.EmailField(
        verbose_name = "E-mail",
        blank = True
    )

    senha = models.CharField(
        max_length = 50,
        verbose_name = "Senha",
        help_text = "Digite aqui a senha..."
    )

    cargo = models.CharField(
        max_length = 50,
        verbose_name = "Cargo",
        help_text = "Digite aqui o cargo..."
    )

class EmpresaParceira(models.Model):
    """Modelo para empresas parceiras com validações aprimoradas"""
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Empresa",
        help_text="Nome completo da empresa parceira"
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ",
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message="CNPJ deve estar no formato: 99.999.999/9999-99"
            )
        ]
    )
    
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone",
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Telefone deve estar no formato: '+999999999'"
            )
        ]
    )
    email = models.EmailField(
        verbose_name="E-mail",
        blank=True
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativa"
    )

    class Meta:
        verbose_name = "Empresa Parceira"
        verbose_name_plural = "Empresas Parceiras"
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cnpj']),
        ]

    def __str__(self):
        return self.nome

class Obra(models.Model):
    """Modelo para obras de construção com status e controle melhorado"""
    STATUS_CHOICES = [
        ('PLANEJAMENTO', 'Planejamento'),
        ('ANDAMENTO', 'Em Andamento'),
        ('PARADA', 'Parada'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Obra"
    )
    empresa = models.ForeignKey(
        EmpresaParceira,
        on_delete=models.CASCADE,
        verbose_name="Empresa Responsável",
        related_name='obras'
    )
    endereco = models.TextField(
        verbose_name="Endereço Completo"
    )
    data_inicio = models.DateField(
        verbose_name="Data de Início"
    )
    data_prevista_termino = models.DateField(
        verbose_name="Previsão de Término",
        blank=True,
        null=True
    )
    data_real_termino = models.DateField(
        verbose_name="Data Real de Término",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='PLANEJAMENTO',
        verbose_name="Status da Obra"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        blank=True
    )

    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        ordering = ['-data_inicio']
        permissions = [
            ('view_obra_report', 'Pode visualizar relatórios de obra'),
        ]

    def __str__(self):
        return f"{self.nome} ({self.empresa})"

    @property
    def dias_atraso(self):
        if self.status == 'CONCLUIDA' and self.data_real_termino and self.data_prevista_termino:
            return (self.data_real_termino - self.data_prevista_termino).days
        return 0

class Colaborador(models.Model):
    """Modelo completo para colaboradores da construção"""
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não informar'),
    ]

    ESTADO_CIVIL_CHOICES = [
        ('SOLTEIRO', 'Solteiro(a)'),
        ('CASADO', 'Casado(a)'),
        ('DIVORCIADO', 'Divorciado(a)'),
        ('VIUVO', 'Viúvo(a)'),
        ('SEPARADO', 'Separado(a)'),
    ]

    # Dados Pessoais
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome Completo"
    )
        
    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CPF",
        validators=[RegexValidator(
            regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
            message="CPF deve estar no formato: 999.999.999-99"
        )]
    )


    rg = models.CharField(
        max_length=20,
        verbose_name="RG",
        blank=True
    )
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name="Sexo"
    )
    estado_civil = models.CharField(
        max_length=10,
        choices=ESTADO_CIVIL_CHOICES,
        verbose_name="Estado Civil",
        blank=True
    )
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone"
    )
    telefone_emergencia = models.CharField(
        max_length=15,
        verbose_name="Telefone de Emergência",
        blank=True
    )
    email = models.EmailField(
        verbose_name="E-mail",
        blank=True
    )
    
    # Endereço
    cep = models.CharField(
        max_length=9,
        verbose_name="CEP"
    )
    logradouro = models.CharField(
        max_length=100,
        verbose_name="Logradouro"
    )
    numero = models.CharField(
        max_length=10,
        verbose_name="Número"
    )
    complemento = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Complemento"
    )
    bairro = models.CharField(
        max_length=50,
        verbose_name="Bairro"
    )
    cidade = models.CharField(
        max_length=50,
        verbose_name="Cidade"
    )
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado"
    )

    # Dados Profissionais
    funcao = models.CharField(
        max_length=100,
        verbose_name="Função/Cargo"
    )
    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Salário"
    )
    data_admissao = models.DateField(
        verbose_name="Data de Admissão",
        default=date.today
    )
    data_demissao = models.DateField(
        verbose_name="Data de Demissão",
        blank=True,
        null=True
    )
    obra = models.ForeignKey(
        Obra,
        on_delete=models.CASCADE,
        verbose_name="Obra Vinculada",
        related_name='colaboradores'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    foto = models.ImageField(
        upload_to='colaboradores/',
        verbose_name="Foto",
        blank=True,
        null=True
    )
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True
    )

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cpf']),
            models.Index(fields=['funcao']),
            models.Index(fields=['ativo']),
        ]
        permissions = [
            ('view_colaborador_report', 'Pode visualizar relatórios de colaboradores'),
        ]

    def __str__(self):
        return f"{self.nome} ({self.funcao})"

    @property
    def tempo_servico(self):
        if self.data_demissao:
            return (self.data_demissao - self.data_admissao).days
        return (date.today() - self.data_admissao).days

class Restaurante(models.Model):
    """Modelo para restaurantes parceiros com avaliação"""
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Restaurante"
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ"
    )
    endereco = models.TextField(
        verbose_name="Endereço Completo"
    )
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone"
    )
    responsavel = models.CharField(
        max_length=100,
        verbose_name="Responsável"
    )
    capacidade = models.IntegerField(
        verbose_name="Capacidade de Atendimento"
    )
    avaliacao = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        verbose_name="Avaliação",
        default=3.0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    data_cadastro = models.DateField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"
        ordering = ['nome']
        constraints = [
            models.CheckConstraint(
                check=models.Q(avaliacao__gte=0) & models.Q(avaliacao__lte=5),
                name="avaliacao_entre_0_e_5"
            )
        ]

    def __str__(self):
        return self.nome

class Refeicao(models.Model):
    """Modelo para registro de refeições com validações"""
    TIPO_REFEICAO_CHOICES = [
        ('CAFE', 'Café da Manhã'),
        ('ALMOCO', 'Almoço'),
        ('JANTA', 'Jantar'),
        ('LANCHE', 'Lanche'),
    ]

    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        verbose_name="Colaborador",
        related_name='refeicoes'
    )
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        verbose_name="Restaurante",
        related_name='refeicoes'
    )
    data = models.DateField(
        verbose_name="Data",
        auto_now_add=True
    )
    horario = models.TimeField(
        verbose_name="Horário",
        auto_now_add=True
    )
    tipo = models.CharField(
        max_length=6,
        choices=TIPO_REFEICAO_CHOICES,
        verbose_name="Tipo de Refeição"
    )
    valor = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Valor da Refeição"
    )
    satisfacao = models.PositiveSmallIntegerField(
        verbose_name="Satisfação (1-5)",
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True
    )

    class Meta:
        verbose_name = "Refeição"
        verbose_name_plural = "Refeições"
        ordering = ['-data', '-horario']
        unique_together = ['colaborador', 'data', 'tipo']
        constraints = [
            models.CheckConstraint(
                check=models.Q(satisfacao__gte=1) & models.Q(satisfacao__lte=5),
                name="satisfacao_entre_1_e_5"
            )
        ]

    def __str__(self):
        return f"{self.colaborador} - {self.get_tipo_display()} em {self.data}"

class RelatorioMensal(models.Model):
    """Modelo para relatórios mensais de refeições com detalhamento"""
    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        verbose_name="Colaborador",
        related_name='relatorios'
    )
    mes_referencia = models.CharField(
        max_length=7,
        verbose_name="Mês de Referência",
        help_text="Formato: AAAA-MM"
    )
    total_refeicoes = models.IntegerField(
        verbose_name="Total de Refeições"
    )
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Total"
    )
    cafe_manha = models.IntegerField(
        verbose_name="Cafés da Manhã",
        default=0
    )
    almocos = models.IntegerField(
        verbose_name="Almoços",
        default=0
    )
    jantares = models.IntegerField(
        verbose_name="Jantares",
        default=0
    )
    lanches = models.IntegerField(
        verbose_name="Lanches",
        default=0
    )
    data_geracao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Geração"
    )
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True
    )

    class Meta:
        verbose_name = "Relatório Mensal"
        verbose_name_plural = "Relatórios Mensais"
        ordering = ['-mes_referencia']
        unique_together = ['colaborador', 'mes_referencia']

    def __str__(self):
        return f"Relatório de {self.mes_referencia} - {self.colaborador}"

    def save(self, *args, **kwargs):
        self.total_refeicoes = self.cafe_manha + self.almocos + self.jantares + self.lanches
        super().save(*args, **kwargs)
        
class Profile(models.Model):
    TIPOS_USUARIO = [
        ('admin', 'Administrador'),
        ('encarregado', 'Encarregado de Obra'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO)
   

    

    def __str__(self):
        return f'{self.user.username} ({self.get_tipo_display()})'

 
