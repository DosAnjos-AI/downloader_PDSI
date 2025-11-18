# Guia de Configuração - Google Drive API

Este guia detalha o processo completo de configuração da Google Drive API para uso com o Downloader PDSI.

**Tempo estimado:** 10-15 minutos
**Requisitos:** Conta Google ativa

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Passo 1: Acessar Google Cloud Console](#passo-1-acessar-google-cloud-console)
3. [Passo 2: Criar ou Selecionar Projeto](#passo-2-criar-ou-selecionar-projeto)
4. [Passo 3: Habilitar Google Drive API](#passo-3-habilitar-google-drive-api)
5. [Passo 4: Configurar Tela de Consentimento OAuth](#passo-4-configurar-tela-de-consentimento-oauth)
6. [Passo 5: Criar Credenciais OAuth2](#passo-5-criar-credenciais-oauth2)
7. [Passo 6: Baixar credentials.json](#passo-6-baixar-credentialsjson)
8. [Passo 7: Primeira Execução e Autenticação](#passo-7-primeira-execução-e-autenticação)
9. [Troubleshooting](#troubleshooting)
10. [Perguntas Frequentes](#perguntas-frequentes)

---

## Visão Geral

O Downloader PDSI utiliza a **Google Drive API** para fazer upload automático de arquivos para o seu Google Drive. Para isso, é necessário:

1. Criar um projeto no Google Cloud Console
2. Habilitar a Google Drive API
3. Configurar tela de consentimento OAuth2
4. Criar credenciais OAuth2 (tipo Desktop App)
5. Baixar arquivo `credentials.json`
6. Autenticar na primeira execução

Este processo é realizado **uma única vez**. Após autenticação inicial, o sistema armazenará token de acesso em `token.pickle` e renovará automaticamente.

**Importante:** O `credentials.json` identifica sua aplicação, mas não dá acesso direto. A autenticação (login) acontece na primeira execução do sistema.

---

## Passo 1: Acessar Google Cloud Console

### 1.1. Abrir o Google Cloud Console

Acesse: [https://console.cloud.google.com/](https://console.cloud.google.com/)

### 1.2. Fazer login

- Use sua conta Google pessoal ou organizacional
- Aceite os termos de serviço se for primeira vez

**Nota:** Se for primeira vez usando Google Cloud Console, pode haver um assistente de boas-vindas. Clique em "Dismiss" ou "Concluir".

---

## Passo 2: Criar ou Selecionar Projeto

### 2.1. Acessar seletor de projetos

No topo da página, clique no nome do projeto atual (ou "Select a project").

### 2.2. Criar novo projeto

**Opção A: Criar novo projeto (recomendado)**

1. Clique em **"NEW PROJECT"** no canto superior direito da janela
2. Preencha os campos:
   - **Project name:** `Downloader PDSI` (ou nome de sua preferência)
   - **Organization:** Deixe como está (No organization)
   - **Location:** Deixe como está
3. Clique em **"CREATE"**
4. Aguarde alguns segundos até o projeto ser criado
5. Você será redirecionado automaticamente para o novo projeto

**Opção B: Usar projeto existente**

1. Selecione projeto existente da lista
2. Clique em **"OPEN"**

**Confirmação:** Verifique no topo da página se o nome do projeto correto está exibido.

---

## Passo 3: Habilitar Google Drive API

### 3.1. Acessar API Library

1. No menu lateral esquerdo, clique em **"APIs & Services"**
2. Clique em **"Library"** (Biblioteca)

Ou acesse diretamente: [https://console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)

### 3.2. Buscar Google Drive API

1. Na barra de busca, digite: `Google Drive API`
2. Clique no resultado **"Google Drive API"** (desenvolvida pelo Google)

### 3.3. Habilitar a API

1. Clique no botão **"ENABLE"** (Ativar)
2. Aguarde alguns segundos até a API ser habilitada
3. Você será redirecionado para a página de overview da API

**Confirmação:** A página deve exibir "API enabled" e gráficos (ainda vazios).

---

## Passo 4: Configurar Tela de Consentimento OAuth

Antes de criar credenciais, é necessário configurar a tela de consentimento que o usuário verá ao autorizar o aplicativo.

### 4.1. Acessar OAuth consent screen

1. No menu lateral esquerdo, clique em **"APIs & Services"**
2. Clique em **"OAuth consent screen"**

Ou acesse diretamente: [https://console.cloud.google.com/apis/credentials/consent](https://console.cloud.google.com/apis/credentials/consent)

### 4.2. Escolher User Type

Selecione **"External"** e clique em **"CREATE"**

**Por quê External?**
- **External:** Qualquer usuário com conta Google pode usar (limitado a 100 usuários em modo teste)
- **Internal:** Apenas usuários da sua organização Google Workspace

Para uso pessoal ou pequena equipe, External é adequado.

### 4.3. Preencher informações do app (Seção 1/4)

Preencha os campos obrigatórios:

**App information:**
- **App name:** `Downloader PDSI` (ou nome de sua preferência)
- **User support email:** Seu email (selecione da lista dropdown)
- **App logo:** (opcional) Deixe em branco

**App domain:** (opcional) Deixe em branco

**Authorized domains:** (opcional) Deixe em branco

**Developer contact information:**
- **Email addresses:** Seu email

Clique em **"SAVE AND CONTINUE"**

### 4.4. Configurar escopos (Seção 2/4)

1. Clique em **"ADD OR REMOVE SCOPES"**
2. Na lista de escopos, procure e marque:
   - `https://www.googleapis.com/auth/drive.file`
   - **Descrição:** "See, edit, create, and delete only the specific Google Drive files you use with this app"
3. Clique em **"UPDATE"** no rodapé
4. Verifique se escopo aparece na tabela
5. Clique em **"SAVE AND CONTINUE"**

**Importante:** Use apenas o escopo `drive.file` (não `drive` completo). Isso limita acesso apenas a arquivos criados pelo app.

### 4.5. Adicionar usuários de teste (Seção 3/4)

Em modo de teste, apenas usuários listados aqui podem autenticar.

1. Clique em **"ADD USERS"**
2. Digite seu email (o mesmo que usará para autenticar)
3. Clique em **"ADD"**
4. Adicione outros emails se necessário (familiares, colegas, etc.)
5. Clique em **"SAVE AND CONTINUE"**

**Nota:** Adicione todos os emails que precisarão usar o sistema. Limite: 100 usuários.

### 4.6. Revisar e confirmar (Seção 4/4)

1. Revise todas as informações
2. Clique em **"BACK TO DASHBOARD"**

**Confirmação:** Status deve exibir "Testing" com ícone de aviso amarelo (isso é normal).

---

## Passo 5: Criar Credenciais OAuth2

### 5.1. Acessar Credentials

1. No menu lateral esquerdo, clique em **"APIs & Services"**
2. Clique em **"Credentials"**

Ou acesse diretamente: [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)

### 5.2. Criar nova credencial

1. Clique no botão **"+ CREATE CREDENTIALS"** no topo
2. Selecione **"OAuth client ID"**

### 5.3. Configurar OAuth client ID

**Se aparecer aviso "To create an OAuth client ID, you must first configure your consent screen":**
- Ignore, já configuramos no Passo 4

Preencha os campos:

1. **Application type:** Selecione **"Desktop app"**
   - **Não selecione** "Web application" ou outras opções

2. **Name:** `Downloader PDSI Desktop` (ou nome de sua preferência)

3. Clique em **"CREATE"**

### 5.4. Credenciais criadas

Uma janela popup aparecerá com as informações:
- **Your Client ID:** (string longa)
- **Your Client Secret:** (string longa)

**Não se preocupe em copiar esses valores agora.** Faremos download do arquivo JSON completo no próximo passo.

Clique em **"OK"** para fechar o popup.

---

## Passo 6: Baixar credentials.json

### 6.1. Localizar a credencial criada

Na página "Credentials", você verá uma tabela "OAuth 2.0 Client IDs" com sua credencial recém-criada.

### 6.2. Baixar JSON

1. Na linha da credencial, no lado direito, clique no ícone de **download** (seta para baixo)
2. Arquivo `client_secret_XXXXX.apps.googleusercontent.com.json` será baixado

### 6.3. Renomear arquivo

1. Localize o arquivo baixado (geralmente na pasta Downloads)
2. Renomeie de `client_secret_XXXXX.apps.googleusercontent.com.json` para **`credentials.json`**

### 6.4. Mover para o projeto

1. Copie o arquivo `credentials.json`
2. Cole na **raiz do projeto downloader_PDSI** (mesmo diretório que `main.py`)

**Estrutura correta:**
```
downloader_PDSI/
├── credentials.json    <-- Arquivo aqui
├── main.py
├── config.py
└── ...
```

**Importante:**
- Nome deve ser exatamente `credentials.json` (minúsculas)
- Deve estar na raiz do projeto
- NUNCA faça commit deste arquivo (já está no .gitignore)

---

## Passo 7: Primeira Execução e Autenticação

### 7.1. Executar o sistema

```bash
python main.py
```

### 7.2. Fluxo de autenticação

1. Sistema detectará `credentials.json`
2. Seu navegador abrirá automaticamente
3. Você verá tela de login do Google

### 7.3. Fazer login

1. Selecione ou digite o email adicionado como usuário de teste (Passo 4.5)
2. Digite sua senha

### 7.4. Aviso de segurança

Você verá uma tela: **"Google hasn't verified this app"**

**Isso é normal!** Seu app está em modo de teste.

1. Clique em **"Advanced"** (Avançado)
2. Clique em **"Go to Downloader PDSI (unsafe)"**

**Por quê "unsafe"?**
- Google marca apps não verificados assim
- Verificação oficial requer processo longo
- Para uso pessoal, modo teste é seguro

### 7.5. Autorizar permissões

Tela exibirá:
- **Downloader PDSI wants to access your Google Account**
- Lista de permissões solicitadas:
  - "See, edit, create, and delete only the specific Google Drive files you use with this app"

1. Revise as permissões
2. Clique em **"Allow"** (Permitir)

### 7.6. Confirmação

- Navegador exibirá: "The authentication flow has completed."
- Pode fechar a aba do navegador
- Terminal exibirá: "[INFO] Autenticacao concluida com sucesso"

### 7.7. Token salvo

Sistema criou arquivo `token.pickle` na raiz do projeto:

```
downloader_PDSI/
├── credentials.json
├── token.pickle        <-- Novo arquivo
├── main.py
└── ...
```

**token.pickle contém:**
- Token de acesso OAuth2
- Token de refresh (para renovação automática)
- Validade de longo prazo

**Importante:** NUNCA faça commit de `token.pickle` (já está no .gitignore)

### 7.8. Próximas execuções

Em execuções futuras:
- Sistema usará `token.pickle` automaticamente
- Navegador NÃO abrirá novamente
- Autenticação é silenciosa e transparente
- Token é renovado automaticamente quando expira

---

## Troubleshooting

### Problema: "credentials.json not found"

**Sintoma:** Erro ao executar sistema.

**Solução:**
1. Verifique se arquivo `credentials.json` existe na raiz
2. Verifique se nome está correto (minúsculas, sem espaços)
3. Verifique se está no diretório correto (raiz do projeto)

---

### Problema: "Access blocked: This app's request is invalid"

**Sintoma:** Erro na tela de autenticação do navegador.

**Causas possíveis:**

**A. Tela de consentimento não configurada**
- Volte ao Passo 4 e configure OAuth consent screen

**B. Email não adicionado como usuário de teste**
- Volte ao Passo 4.5
- Adicione seu email na lista de test users
- Use o mesmo email na autenticação

**C. Escopo incorreto**
- Volte ao Passo 4.4
- Verifique se escopo `drive.file` está adicionado

---

### Problema: "The authentication flow has completed" mas sistema não continua

**Sintoma:** Navegador exibe mensagem de sucesso mas terminal trava.

**Solução:**
1. Verifique se apareceu mensagem de erro no terminal
2. Verifique se arquivo `token.pickle` foi criado
3. Se não foi criado, delete `token.pickle` (se existir) e tente novamente
4. Verifique conexão com internet
5. Tente executar novamente: `python main.py`

---

### Problema: "invalid_grant" ao renovar token

**Sintoma:** Erro ao executar sistema com token.pickle existente.

**Causa:** Token expirou ou foi revogado.

**Solução:**
1. Delete arquivo `token.pickle`:
   ```bash
   rm token.pickle
   ```
2. Execute novamente: `python main.py`
3. Autentique novamente no navegador

---

### Problema: "Rate limit exceeded" durante configuração

**Sintoma:** Erro ao tentar criar projeto ou habilitar API.

**Causa:** Muitas requisições em curto período.

**Solução:**
- Aguarde 5-10 minutos
- Tente novamente
- Se persistir, aguarde até próximo dia

---

### Problema: Navegador não abre automaticamente

**Sintoma:** Sistema fica aguardando mas navegador não abre.

**Solução:**

**Opção 1:** Copiar URL manualmente
1. Terminal exibirá URL longa começando com `https://accounts.google.com/o/oauth2/auth?...`
2. Copie URL completa
3. Cole no navegador
4. Complete autenticação

**Opção 2:** Verificar navegador padrão
1. Configure navegador padrão do sistema
2. Execute novamente

---

### Problema: "Insufficient authentication scopes"

**Sintoma:** Erro ao tentar fazer upload para Drive.

**Causa:** Escopo OAuth2 incorreto.

**Solução:**
1. Delete `token.pickle`
2. Volte ao Passo 4.4
3. Verifique escopo `drive.file`
4. Delete credencial OAuth2 atual (Passo 5.1, clique na lixeira)
5. Crie nova credencial (repita Passos 5 e 6)
6. Execute sistema e autentique novamente

---

## Perguntas Frequentes

### P1: Preciso pagar para usar Google Drive API?

**R:** Não. Google Drive API tem cota gratuita generosa suficiente para uso pessoal. Limites:
- 20.000 requisições por dia (projeto)
- 1.000 requisições por 100 segundos (usuário)

Para uso típico do Downloader PDSI (dezenas de uploads por dia), limites são mais que suficientes.

### P2: Preciso publicar meu app para sair do modo teste?

**R:** Não para uso pessoal. Modo teste permite 100 usuários, suficiente para uso individual ou pequena equipe. Publicação é necessária apenas para apps públicos.

### P3: Quanto tempo o token.pickle é válido?

**R:** Tokens OAuth2 são de longa duração e renováveis. Sistema renova automaticamente. Em condições normais, `token.pickle` dura indefinidamente.

### P4: Posso usar mesmas credenciais em vários computadores?

**R:** Sim. Copie `credentials.json` para outros computadores. Cada computador terá seu próprio `token.pickle` após primeira autenticação.

### P5: E se eu deletar token.pickle acidentalmente?

**R:** Sem problemas. Execute `python main.py` e autentique novamente. Novo token será gerado. Arquivos no Drive não são afetados.

### P6: Posso revogar acesso do app?

**R:** Sim. Acesse [myaccount.google.com/permissions](https://myaccount.google.com/permissions), encontre "Downloader PDSI" e clique em "Remove Access". Após revogar, delete `token.pickle` e autentique novamente se quiser reativar.

### P7: credentials.json expõe minha senha do Google?

**R:** Não. `credentials.json` identifica seu app, mas não contém senhas. Senha é solicitada apenas durante autenticação (no navegador), nunca é armazenada no sistema.

### P8: O que acontece se credentials.json vazar?

**R:** `credentials.json` contém `client_secret`, que não dá acesso direto ao Drive, mas permite que terceiros criem tokens em nome do seu app. Se vazar:
1. Acesse Credentials no Cloud Console
2. Delete a credencial comprometida
3. Crie nova credencial (repita Passos 5 e 6)
4. Substitua `credentials.json`

### P9: Posso ter múltiplos usuários autenticados?

**R:** Cada instalação do sistema tem um `token.pickle` vinculado a um usuário. Para múltiplos usuários:
- Opção A: Cada usuário tem sua instalação separada
- Opção B: Deletar `token.pickle` e reautenticar quando trocar usuário

### P10: Preciso renovar algo periodicamente?

**R:** Não. Sistema gerencia renovação de tokens automaticamente. Configuração é one-time setup.

---

## Recursos Adicionais

### Documentação Oficial:

- **Google Drive API Overview:** [developers.google.com/drive/api/guides/about-sdk](https://developers.google.com/drive/api/guides/about-sdk)
- **Python Quickstart:** [developers.google.com/drive/api/quickstart/python](https://developers.google.com/drive/api/quickstart/python)
- **OAuth 2.0:** [developers.google.com/identity/protocols/oauth2](https://developers.google.com/identity/protocols/oauth2)
- **API Reference:** [developers.google.com/drive/api/reference/rest/v3](https://developers.google.com/drive/api/reference/rest/v3)

### Vídeos Tutoriais:

- **Criar projeto no Google Cloud Console:** Busque "google cloud console create project" no YouTube
- **Habilitar APIs:** Busque "enable google drive api" no YouTube
- **OAuth 2.0 explained:** Busque "oauth2 flow explained" no YouTube

### Suporte:

- **Issues do Projeto:** [github.com/DosAnjos-AI/downloader_PDSI/issues](https://github.com/DosAnjos-AI/downloader_PDSI/issues)
- **Stack Overflow:** Tag `google-drive-api` e `python`
- **Google Cloud Support:** [cloud.google.com/support](https://cloud.google.com/support)

---

## Checklist de Configuração

Use este checklist para garantir que tudo foi configurado corretamente:

- [ ] Acessei Google Cloud Console
- [ ] Criei ou selecionei projeto
- [ ] Habilitei Google Drive API
- [ ] Configurei OAuth consent screen (External)
- [ ] Adicionei meu email como usuário de teste
- [ ] Adicionei escopo `drive.file`
- [ ] Criei credencial OAuth2 tipo Desktop App
- [ ] Baixei arquivo JSON
- [ ] Renomeei para `credentials.json`
- [ ] Movi para raiz do projeto downloader_PDSI
- [ ] Executei `python main.py`
- [ ] Navegador abriu e fiz login
- [ ] Cliquei em "Advanced" e "Go to Downloader PDSI"
- [ ] Autorizei permissões
- [ ] Navegador exibiu "authentication flow completed"
- [ ] Arquivo `token.pickle` foi criado
- [ ] Sistema continua execução normalmente

**Se todos os itens estão marcados: Configuração concluída com sucesso!**

---

## Próximos Passos

Após configuração bem-sucedida:

1. **Configure config.py:** Ajuste parâmetros conforme seu caso de uso
2. **Teste com poucos vídeos:** Processe 2-3 vídeos para validar
3. **Verifique Google Drive:** Confirme criação de pasta BD_PDSI
4. **Monitore logs:** Acompanhe logs/processing.log e logs/errors.log
5. **Processe volumes maiores:** Após validação, processe playlists/canais completos

**Boa utilização do Downloader PDSI!**

---

**Versão do guia:** 1.0
**Última atualização:** 2024-01-15
**Feedback:** [GitHub Issues](https://github.com/DosAnjos-AI/downloader_PDSI/issues)
