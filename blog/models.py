from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    slug = models.SlugField('Slug', max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    titulo = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=False, blank=True)  # Temporarily non-unique
    conteudo = models.TextField('Conteúdo', help_text='Use HTML para formatação')
    data_publicacao = models.DateTimeField('Data de Publicação', default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    categorias = models.ManyToManyField(Category, verbose_name='Categorias', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-data_publicacao']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    texto = models.TextField('Comentário')
    data_criacao = models.DateTimeField('Data de Criação', default=timezone.now)
    aprovado = models.BooleanField('Aprovado', default=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-data_criacao']

    def __str__(self):
        return f'Comentário de {self.autor.username} em {self.post.titulo}'
        
    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.id}"
