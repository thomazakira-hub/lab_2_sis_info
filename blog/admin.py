from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'post_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def description_short(self, obj):
        return obj.description[:100] + '...' if obj.description else ''
    description_short.short_description = 'Descrição'
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Nº de Posts'


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
    
    categorias = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple(
            verbose_name=_('Categorias'),
            is_stacked=False
        ),
        required=False
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('titulo', 'autor', 'data_publicacao', 'comment_count', 'display_categories')
    list_filter = ('data_publicacao', 'autor', 'categorias')
    search_fields = ('titulo', 'conteudo', 'categorias__name')
    filter_horizontal = ('categorias',)
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'data_publicacao'
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comentários'
    
    def display_categories(self, obj):
        return ", ".join([c.name for c in obj.categorias.all()])
    display_categories.short_description = 'Categorias'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('texto_truncado', 'post_link', 'autor', 'data_criacao', 'aprovado')
    list_filter = ('aprovado', 'data_criacao')
    search_fields = ('texto', 'autor__username', 'post__titulo')
    actions = ['approve_comments']
    
    def texto_truncado(self, obj):
        return f"{obj.texto[:50]}..." if len(obj.texto) > 50 else obj.texto
    texto_truncado.short_description = 'Comentário'
    
    def post_link(self, obj):
        url = obj.post.get_absolute_url()
        return format_html('<a href="{}">{}</a>', url, obj.post.titulo)
    post_link.short_description = 'Post'
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(aprovado=True)
        self.message_user(request, f'{updated} comentário(s) aprovado(s) com sucesso!')
    approve_comments.short_description = 'Aprovar comentários selecionados'
    ordering = ('-data_criacao',)
