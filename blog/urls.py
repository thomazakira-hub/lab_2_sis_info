from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Lista de posts (com filtro opcional por categoria)
    path('categoria/<slug:category_slug>/', views.post_list, name='post_list_by_category'),
    path('', views.post_list, name='post_list'),
    
    # Detalhes de um post
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # Criar novo post
    path('post/novo/', views.post_create, name='post_create'),
    
    # Editar post existente
    path('post/<int:pk>/editar/', views.post_edit, name='post_edit'),
    
    # Deletar post
    path('post/<int:pk>/deletar/', views.post_delete, name='post_delete'),
]
