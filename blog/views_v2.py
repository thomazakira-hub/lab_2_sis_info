from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import Http404, HttpResponseForbidden
from .models import Post
from .forms import PostForm

def post_list(request):
    """Lista todos os posts publicados."""
    posts = Post.objects.all().order_by('-data_publicacao')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """Exibe os detalhes de um post específico."""
    try:
        post = get_object_or_404(Post, pk=pk)
    except Post.DoesNotExist:
        raise Http404("O post solicitado não existe.")
    return render(request, 'blog/post_detail.html', {'post': post})

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
            post = form.save()
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
