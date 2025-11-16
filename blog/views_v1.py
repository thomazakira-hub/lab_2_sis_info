from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import Http404
from .models import Post

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
    """Cria um novo post."""
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        conteudo = request.POST.get('conteudo', '').strip()
        
        if titulo and conteudo:
            post = Post.objects.create(
                titulo=titulo,
                conteudo=conteudo,
                autor=request.user,
                data_publicacao=timezone.now()
            )
            messages.success(request, 'Post criado com sucesso!')
            return redirect('blog:post_detail', pk=post.pk)
        else:
            messages.error(request, 'Título e conteúdo são obrigatórios.')
    
    return render(request, 'blog/post_form.html', {'titulo_pagina': 'Novo Post'})

@login_required
def post_edit(request, pk):
    """Edita um post existente."""
    post = get_object_or_404(Post, pk=pk)
    
    # Verifica se o usuário é o autor do post
    if post.autor != request.user:
        messages.error(request, 'Você não tem permissão para editar este post.')
        return redirect('blog:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        conteudo = request.POST.get('conteudo', '').strip()
        
        if titulo and conteudo:
            post.titulo = titulo
            post.conteudo = conteudo
            post.save()
            messages.success(request, 'Post atualizado com sucesso!')
            return redirect('blog:post_detail', pk=post.pk)
        else:
            messages.error(request, 'Título e conteúdo são obrigatórios.')
    
    return render(request, 'blog/post_form.html', {
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
