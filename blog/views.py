from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm

def post_list(request, category_slug=None):
    """Lista todos os posts publicados, opcionalmente filtrados por categoria."""
    category = None
    categories = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    posts = Post.objects.all().order_by('-data_publicacao')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(categorias=category)
    
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'category': category,
        'categories': categories
    })

def post_detail(request, pk):
    """Exibe os detalhes de um post específico e seus comentários."""
    try:
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.filter(aprovado=True).order_by('-data_criacao')
        
        # Novo comentário
        if request.method == 'POST' and 'comment_submit' in request.POST:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # Cria o comentário, mas não salva ainda
                new_comment = comment_form.save(commit=False)
                # Atribui o post e o autor ao comentário
                new_comment.post = post
                new_comment.autor = request.user
                # Salva o comentário
                new_comment.save()
                messages.success(request, 'Seu comentário foi enviado e está aguardando aprovação.')
                return HttpResponseRedirect(post.get_absolute_url())
        else:
            comment_form = CommentForm()
            
    except Post.DoesNotExist:
        raise Http404("O post solicitado não existe.")
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def post_create(request):
    """Cria um novo post usando o formulário Django."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.data_publicacao = timezone.now()
            post.save()
            
            # Salva as categorias (many-to-many)
            form.save_m2m()
            
            messages.success(request, 'Post criado com sucesso!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'titulo_pagina': 'Novo Post'
    })

@login_required
def post_edit(request, pk):
    """Edita um post existente usando o formulário Django."""
    post = get_object_or_404(Post, pk=pk)
    
    # Verifica se o usuário é o autor do post
    if post.autor != request.user:
        messages.error(request, 'Você não tem permissão para editar este post.')
        return redirect('blog:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            
            # Salva as categorias (many-to-many)
            form.save_m2m()
            
            messages.success(request, 'Post atualizado com sucesso!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'post': post,
        'titulo_pagina': 'Editar Post'
    })

@login_required
def post_delete(request, pk):
    """Exclui um post."""
    post = get_object_or_404(Post, pk=pk)
    
    # Verifica se o usuário é o autor do post
    if post.autor != request.user:
        messages.error(request, 'Você não tem permissão para excluir este post.')
        return redirect('blog:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post excluído com sucesso!')
        return redirect('blog:post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
