# Guia de Deploy no Render

Este documento explica como fazer o deploy deste projeto Django no Render.

## Pré-requisitos

1. Conta no [Render](https://render.com)
2. Repositório Git configurado (GitHub, GitLab, etc.)
3. Projeto configurado e pronto para produção

## Configurações já realizadas

✅ **settings.py** configurado para usar variáveis de ambiente
✅ **WhiteNoise** configurado para servir arquivos estáticos
✅ **dj-database-url** configurado para conectar ao PostgreSQL
✅ **render.yaml** preparado com as configurações necessárias
✅ **build.sh** criado para build e migrações automáticas
✅ **requirements.txt** com todas as dependências

## Passos para Deploy

### 1. Criar Banco de Dados PostgreSQL no Render

1. Acesse o [Dashboard do Render](https://dashboard.render.com)
2. Clique em "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `blog-db` (ou outro nome, mas deve corresponder ao nome no `render.yaml`)
   - **Database**: `blogdb` (ou outro nome)
   - **User**: Deixe o padrão
   - **Region**: Escolha a região mais próxima
   - **Plan**: Free (para testes) ou Starter (recomendado para produção)
4. Clique em "Create Database"
5. Anote as informações de conexão (elas serão usadas automaticamente)

### 2. Criar Serviço Web no Render

#### Opção A: Usando render.yaml (Recomendado)

1. No Dashboard do Render, clique em "New +" → "Blueprint"
2. Conecte seu repositório Git
3. Render detectará automaticamente o arquivo `render.yaml`
4. O serviço será criado automaticamente com todas as configurações

#### Opção B: Configuração Manual

1. No Dashboard do Render, clique em "New +" → "Web Service"
2. Conecte seu repositório Git
3. Configure:
   - **Name**: `meu-blog-django` (ou o nome que preferir)
   - **Region**: Mesma região do banco de dados
   - **Branch**: `main` (ou sua branch principal)
   - **Root Directory**: Deixe vazio (raiz do projeto)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
   - **Plan**: Free (para testes) ou Starter (recomendado)

### 3. Configurar Variáveis de Ambiente

Se você não usou o `render.yaml`, configure manualmente:

1. No painel do seu Web Service, vá em "Environment"
2. Adicione as seguintes variáveis:

```
SECRET_KEY = <Gere uma chave secreta>
DATABASE_URL = <URL do banco de dados criado>
ALLOWED_HOSTS = <nome-do-seu-servico>.onrender.com
DEBUG = False
PYTHON_VERSION = 3.9.13
```

**Para gerar uma SECRET_KEY:**
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Para obter a DATABASE_URL:**
- No painel do seu banco de dados PostgreSQL no Render, vá em "Connections"
- Copie a "Internal Database URL" ou "External Database URL"
- Use a Internal Database URL para melhor performance

### 4. Criar Superusuário (Administrador)

Após o primeiro deploy bem-sucedido:

1. No painel do Web Service, abra o "Shell"
2. Execute:
```bash
python manage.py createsuperuser
```
3. Siga as instruções para criar seu usuário administrador

### 5. Atualizar ALLOWED_HOSTS no render.yaml

Se você escolher um nome diferente para o serviço, atualize o `render.yaml`:

```yaml
- key: ALLOWED_HOSTS
  value: "seu-servico.onrender.com"
```

## Verificação pós-deploy

1. Acesse a URL do seu serviço (ex: `https://meu-blog-django.onrender.com`)
2. Verifique se o site está funcionando
3. Acesse `/admin` e faça login com o superusuário criado
4. Verifique se os arquivos estáticos estão sendo servidos corretamente

## Troubleshooting

### Erro de migrações
- Verifique os logs no Render
- Execute manualmente: `python manage.py migrate` no Shell

### Arquivos estáticos não aparecem
- Verifique se o `collectstatic` está sendo executado no build
- Verifique os logs de build para erros no `collectstatic`

### Erro de conexão com banco de dados
- Verifique se a variável `DATABASE_URL` está configurada corretamente
- Verifique se o banco de dados está no mesmo plano que o serviço web

### Timeout no build
- O plano Free pode ter limitações
- Considere usar um plano Starter para melhor performance

## Notas Importantes

⚠️ **Plano Free do Render:**
- Serviços podem "adormecer" após 15 minutos de inatividade
- Primeira requisição após dormir pode levar alguns segundos
- Não é recomendado para produção

⚠️ **Segurança:**
- Nunca commite arquivos `.env` ou `SECRET_KEY` no Git
- Sempre use variáveis de ambiente no Render
- Mantenha `DEBUG=False` em produção

⚠️ **Arquivos de Mídia:**
- No plano Free do Render, o armazenamento é efêmero (arquivos podem ser perdidos)
- Arquivos de mídia (`MEDIA_ROOT`) não são persistentes
- Para produção, considere usar um serviço de armazenamento como:
  - AWS S3
  - Cloudinary
  - Azure Blob Storage
  - Outros serviços compatíveis com Django (django-storages)

## Comandos úteis

- **Ver logs**: No painel do serviço → "Logs"
- **Shell**: No painel do serviço → "Shell"
- **Migrations**: No Shell → `python manage.py migrate`
- **Collectstatic**: No Shell → `python manage.py collectstatic --no-input`

## Suporte

Para mais informações, consulte:
- [Documentação do Render](https://render.com/docs)
- [Deploy Django no Render](https://render.com/docs/deploy-django)

