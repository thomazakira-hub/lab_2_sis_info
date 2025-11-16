from django import forms
from django.forms import CheckboxSelectMultiple
from .models import Post, Comment, Category

class PostForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Categorias'
    )
    
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'categorias']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do post',
                'required': True
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conteúdo do post (use HTML para formatação)',
                'rows': 10,
                'required': True
            }),
        }
        help_texts = {
            'conteudo': 'Use HTML para formatar o conteúdo do post. Exemplos: &lt;strong&gt;negrito&lt;/strong&gt;, &lt;em&gt;itálico&lt;/em&gt;, &lt;a href="URL"&gt;link&lt;/a&gt;',
        }
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if not titulo:
            raise forms.ValidationError('O título é obrigatório.')
        return titulo
    
    def clean_conteudo(self):
        conteudo = self.cleaned_data.get('conteudo', '').strip()
        if not conteudo:
            raise forms.ValidationError('O conteúdo é obrigatório.')
        return conteudo


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deixe seu comentário...',
                'rows': 3,
                'required': True
            })
        }
    
    def clean_texto(self):
        texto = self.cleaned_data.get('texto', '').strip()
        if not texto:
            raise forms.ValidationError('O comentário não pode estar vazio.')
        return texto
