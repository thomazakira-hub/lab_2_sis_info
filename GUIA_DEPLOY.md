# 🚀 Guia Completo de Deploy no Render

Este guia vai te levar do zero até ter sua aplicação Django rodando no Render.

## 📋 Pré-requisitos

- Conta no [Render](https://render.com) (grátis)
- Conta no GitLab (já tem: https://gitlab.uspdigital.usp.br/pmr3304450339/lab_2_sis_info.git)
- Git instalado no seu computador

---

## 🔧 PASSO 1: Preparar o Repositório Git Local

### 1.1 Inicializar o Git (se ainda não estiver inicializado)

Abra o terminal na pasta do projeto e execute:

```bash
# Inicializar o repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Configuração inicial para deploy no Render"
```

### 1.2 Conectar ao Repositório GitLab

```bash
# Adicionar o repositório remoto do GitLab
git remote add origin https://gitlab.uspdigital.usp.br/pmr3304450339/lab_2_sis_info.git

# Renomear a branch para main (se necessário)
git branch -M main

# Fazer push para o GitLab
git push -u origin main
```

**Nota:** Se você já tem arquivos no GitLab, pode precisar fazer `git pull` primeiro ou usar `git push -uf origin main` para forçar o push.

---

## 🌐 PASSO 2: Criar Conta no Render

1. Acesse [https://render.com](https://render.com)
2. Clique em **"Get Started for Free"** ou **"Sign Up"**
3. Faça login com GitHub, GitLab ou email
4. Confirme seu email se necessário

---

## 🔗 PASSO 3: Conectar o Repositório GitLab ao Render

1. No Dashboard do Render, clique em **"New +"** (canto superior direito)
2. Selecione **"Blueprint"** (a opção mais fácil!)
3. Na tela de conexão:
   - Se você já conectou o GitLab antes, selecione o repositório `lab_2_sis_info`
   - Se não, clique em **"Connect account"** ou **"Configure GitLab"**
   - Autorize o Render a acessar seu GitLab
   - Selecione o repositório: `pmr3304450339/lab_2_sis_info`
4. Clique em **"Connect"**

---

## ⚙️ PASSO 4: Configurar o Deploy (Automático com Blueprint)

O Render vai detectar automaticamente o arquivo `render.yaml` no seu projeto!

1. O Render mostrará uma prévia das configurações:
   - **Web Service**: `meu-blog-django`
   - **Database**: `blog-db` (PostgreSQL)
   - Todas as variáveis de ambiente já configuradas

2. **IMPORTANTE:** Verifique se:
   - O nome do serviço está correto (ou altere se quiser)
   - A branch está como `main` (ou a branch que você usa)
   - O plano está como **Free** (para começar)

3. Clique em **"Apply"** ou **"Create Blueprint"**

---

## ⏳ PASSO 5: Aguardar o Deploy

O Render vai:
1. ✅ Criar o banco de dados PostgreSQL automaticamente
2. ✅ Instalar todas as dependências do `requirements.txt`
3. ✅ Executar as migrações do banco de dados
4. ✅ Coletar arquivos estáticos
5. ✅ Iniciar o servidor com Gunicorn

**Tempo estimado:** 5-10 minutos na primeira vez

Você pode acompanhar o progresso na aba **"Logs"** do seu serviço.

---

## 👤 PASSO 6: Criar Superusuário (Administrador)

Após o deploy ser concluído com sucesso:

1. No Dashboard do Render, clique no seu serviço web (`meu-blog-django`)
2. Vá na aba **"Shell"** (no menu lateral)
3. Clique em **"Open Shell"**
4. Execute o comando:

```bash
python manage.py createsuperuser
```

5. Siga as instruções:
   - **Username:** (escolha um nome de usuário)
   - **Email:** (seu email)
   - **Password:** (escolha uma senha forte)

---

## ✅ PASSO 7: Verificar se Está Funcionando

1. No Dashboard do Render, clique no seu serviço web
2. Você verá a URL do seu site (ex: `https://meu-blog-django.onrender.com`)
3. Clique na URL ou copie e cole no navegador
4. Teste:
   - ✅ Acesse a página inicial
   - ✅ Acesse `/admin` e faça login com o superusuário criado
   - ✅ Verifique se os arquivos estáticos (CSS, JS) estão carregando

---

## 🔄 Atualizações Futuras

Sempre que você fizer alterações no código:

```bash
# Fazer commit das alterações
git add .
git commit -m "Descrição das alterações"
git push origin main
```

O Render vai **automaticamente** detectar o push e fazer um novo deploy! 🎉

---

## 🐛 Solução de Problemas Comuns

### ❌ Erro: "Build failed"

**Solução:**
- Verifique os logs no Render (aba "Logs")
- Certifique-se de que todas as dependências estão no `requirements.txt`
- Verifique se o `build.sh` tem permissão de execução (o Render cuida disso automaticamente)

### ❌ Erro: "Database connection failed"

**Solução:**
- Verifique se o banco de dados foi criado (deve aparecer no Dashboard)
- Verifique se o nome do banco no `render.yaml` está correto: `blog-db`
- Aguarde alguns minutos após criar o banco (pode levar tempo para inicializar)

### ❌ Erro: "Static files not found"

**Solução:**
- Verifique os logs do build para ver se `collectstatic` foi executado
- Certifique-se de que o `build.sh` inclui `python manage.py collectstatic --no-input`

### ❌ Site não carrega após deploy

**Solução:**
- Verifique se o serviço está "Live" (não "Sleeping")
- No plano Free, o serviço "dorme" após 15 minutos de inatividade
- A primeira requisição após dormir pode levar alguns segundos

### ❌ Erro 500 Internal Server Error

**Solução:**
- Verifique os logs do serviço no Render
- Certifique-se de que as migrações foram executadas
- Verifique se o `SECRET_KEY` foi gerado automaticamente

---

## 📝 Notas Importantes

⚠️ **Plano Free do Render:**
- Serviços podem "adormecer" após 15 minutos de inatividade
- Primeira requisição após dormir pode levar 30-60 segundos
- Não é recomendado para produção com muitos usuários

⚠️ **Arquivos de Mídia:**
- No plano Free, arquivos enviados (imagens, etc.) podem ser perdidos
- Para produção, considere usar AWS S3, Cloudinary ou similar

⚠️ **Banco de Dados:**
- O banco PostgreSQL é criado automaticamente pelo `render.yaml`
- Dados são persistentes mesmo no plano Free
- Backup automático no plano Starter ou superior

---

## 🎉 Pronto!

Sua aplicação Django está no ar! 🚀

**URL do seu site:** `https://meu-blog-django.onrender.com` (ou o nome que você escolheu)

**Próximos passos:**
- Personalize o nome do serviço se quiser
- Configure um domínio personalizado (opcional)
- Faça melhorias e faça push - o deploy é automático!

---

## 📞 Precisa de Ajuda?

- [Documentação do Render](https://render.com/docs)
- [Deploy Django no Render](https://render.com/docs/deploy-django)
- Logs do serviço no Dashboard do Render


