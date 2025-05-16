from django.contrib import admin
from django.utils.html import format_html
from .models import (Profile, EmpresaParceira, Obra, Colaborador, 
                    Restaurante, Refeicao, RelatorioMensal)



class EmpresaParceiraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone', 'email', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'cnpj')
    list_per_page = 20
    ordering = ('nome',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cnpj', 'ativo')
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
        }),
    )

class ObraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'status', 'data_inicio', 
                   'data_prevista_termino', 'dias_atraso_display')
    list_filter = ('status', 'empresa', 'data_inicio')
    search_fields = ('nome', 'empresa__nome')
    date_hierarchy = 'data_inicio'
    raw_id_fields = ('empresa',)
    list_per_page = 30
    ordering = ('-data_inicio',)
    
    fieldsets = (
        ('Identificação', {
            'fields': ('nome', 'empresa', 'status')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_prevista_termino', 'data_real_termino')
        }),
        ('Localização', {
            'fields': ('endereco',)
        }),
        ('Detalhes', {
            'fields': ('descricao',)
        }),
    )
    
    def dias_atraso_display(self, obj):
        return obj.dias_atraso or '-'
    dias_atraso_display.short_description = 'Dias de Atraso'

class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'funcao', 'obra', 'data_admissao', 
                   'tempo_servico_display', 'ativo', 'foto_display')
    list_filter = ('ativo', 'funcao', 'sexo', 'obra')
    search_fields = ('nome', 'cpf', 'funcao')
    date_hierarchy = 'data_admissao'
    raw_id_fields = ('obra',)
    list_per_page = 50
    ordering = ('nome',)
    readonly_fields = ('foto_display',)
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': (
                'foto', 'foto_display', 'nome', 'cpf', 'rg',
                'data_nascimento', 'sexo', 'estado_civil'
            )
        }),
        ('Contato', {
            'fields': ('telefone', 'telefone_emergencia', 'email')
        }),
        ('Endereço', {
            'fields': (
                'cep', 'logradouro', 'numero', 'complemento',
                'bairro', 'cidade', 'estado'
            )
        }),
        ('Dados Profissionais', {
            'fields': (
                'funcao', 'salario', 'data_admissao', 
                'data_demissao', 'obra', 'ativo'
            )
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )
    
    def tempo_servico_display(self, obj):
        return f"{obj.tempo_servico} dias"
    tempo_servico_display.short_description = 'Tempo de Serviço'
    
    def foto_display(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" />', obj.foto.url)
        return "-"
    foto_display.short_description = 'Foto Atual'

class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel', 'telefone', 
                   'avaliacao', 'capacidade', 'ativo')
    list_filter = ('ativo', 'avaliacao')
    search_fields = ('nome', 'cnpj', 'responsavel')
    list_editable = ('avaliacao',)
    list_per_page = 20
    
    fieldsets = (
        ('Identificação', {
            'fields': ('nome', 'cnpj', 'ativo')
        }),
        ('Informações', {
            'fields': ('responsavel', 'capacidade', 'avaliacao')
        }),
        ('Contato', {
            'fields': ('telefone', 'endereco')
        }),
    )

class RefeicaoAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'tipo', 'restaurante', 
                   'data', 'horario', 'valor', 'satisfacao_display')
    list_filter = ('tipo', 'restaurante', 'data')
    search_fields = ('colaborador__nome', 'restaurante__nome')
    date_hierarchy = 'data'
    raw_id_fields = ('colaborador', 'restaurante')
    list_per_page = 50
    
    def satisfacao_display(self, obj):
        if obj.satisfacao:
            return f"{obj.satisfacao} ★"
        return "-"
    satisfacao_display.short_description = 'Satisfação'

class RelatorioMensalAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'mes_referencia', 'total_refeicoes', 
                   'valor_total', 'data_geracao')
    list_filter = ('mes_referencia',)
    search_fields = ('colaborador__nome',)
    date_hierarchy = 'data_geracao'
    raw_id_fields = ('colaborador',)
    readonly_fields = ('data_geracao',)
    
    fieldsets = (
        ('Identificação', {
            'fields': ('colaborador', 'mes_referencia')
        }),
        ('Quantitativos', {
            'fields': (
                'cafe_manha', 'almocos', 'jantares', 'lanches',
                'total_refeicoes', 'valor_total'
            )
        }),
        ('Detalhes', {
            'fields': ('data_geracao', 'observacoes')
        }),
    )
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo')
    list_filter = ('tipo', )
    search_fields = ('user__username', 'user__email')
# Registro dos modelos
admin.site.register(EmpresaParceira, EmpresaParceiraAdmin)
admin.site.register(Obra, ObraAdmin)
admin.site.register(Colaborador, ColaboradorAdmin)
admin.site.register(Restaurante, RestauranteAdmin)
admin.site.register(Refeicao, RefeicaoAdmin)
admin.site.register(RelatorioMensal, RelatorioMensalAdmin)

