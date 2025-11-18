# Downloader PDSI

Sistema local de download de áudios do YouTube com upload automático para Google Drive

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Repositório:** [github.com/DosAnjos-AI/downloader_PDSI](https://github.com/DosAnjos-AI/downloader_PDSI)

---

## Descrição

O **Downloader PDSI** é um sistema completo para download automatizado de áudios do YouTube com integração nativa ao Google Drive. O sistema realiza download local temporário, extração de metadados completos, e upload automático para o Google Drive seguindo estrutura organizada e padronizada.

Desenvolvido para casos de uso acadêmico e profissional, o sistema oferece controle granular sobre qualidade, formato, durações, delays e organização de arquivos. Ideal para projetos de pesquisa, curadoria de conteúdo, backup de material educacional e construção de bases de dados de áudio.

**Principais funcionalidades:**
- Download local de áudios em diversos formatos e qualidades
- Suporte para vídeos individuais, playlists completas e canais
- Extração automática de metadados completos (CSV + JSON)
- Upload automático e organizado para Google Drive
- Sistema de skip inteligente (não reprocessa IDs já baixados)
- Limpeza automática de arquivos temporários após upload
- Logs persistentes e sistema de retry robusto

---

## Funcionalidades

- **Download local de áudios:** Suporte para vídeos, playlists e canais do YouTube
- **Múltiplos formatos:** mp3, flac, wav, m4a, opus, ogg e outros
- **Controle de qualidade:** Configuração de bitrate (128k, 192k, 256k, 320k, best)
- **Filtros de duração:** Define duração mínima e máxima dos vídeos
- **Extração de metadados:** CSV consolidado + JSON individual por vídeo
- **Upload automático Google Drive:** Estrutura organizada com pastas por vídeo
- **Sistema de skip inteligente:** Não reprocessa IDs já baixados (via logs/downloaded_ids.json)
- **Suporte a batch:** Processa múltiplos links de um arquivo .txt
- **Delay randômico:** Intervalo configurável entre downloads para evitar rate limiting
- **Limpeza automática:** Remove arquivos temporários após upload bem-sucedido
- **Logs persistentes:** Rastreamento completo de processamento e erros
- **Sistema de retry:** Tentativas automáticas em caso de falhas de download ou upload
- **Validação robusta:** Verifica configurações antes de iniciar processamento

---

## Requisitos

- **Python 3.8 ou superior**
- **Conta Google ativa** com acesso ao Google Drive
- **Espaço disponível no Google Drive** (depende do volume de downloads)
- **Conexão com internet** estável
- **Sistema operacional:** Linux, macOS ou Windows

---

## Instalação

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/DosAnjos-AI/downloader_PDSI.git
cd downloader_PDSI
```

### Passo 2: Criar ambiente virtual (recomendado)

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar dependências

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

**Dependências instaladas:**
- `yt-dlp` - Download e extração de metadados do YouTube
- `google-api-python-client` - Cliente oficial Google Drive API
- `google-auth-oauthlib` - Autenticação OAuth2
- `google-auth-httplib2` - Adaptador HTTP autenticado
- `pandas` - Manipulação de dados CSV

---

## Configuração Google Drive API

Antes de usar o sistema, é necessário configurar as credenciais OAuth2 da Google Drive API.

**Tempo estimado:** 10-15 minutos
**Guia detalhado:** [SETUP.md](SETUP.md)

### Resumo dos passos principais:

1. Acessar [Google Cloud Console](https://console.cloud.google.com/)
2. Criar novo projeto ou selecionar projeto existente
3. Habilitar **Google Drive API** no projeto
4. Configurar tela de consentimento OAuth2 (tipo External)
5. Adicionar seu email como usuário de teste
6. Criar credenciais OAuth2 (tipo "Desktop App")
7. Baixar arquivo `credentials.json`
8. Colocar `credentials.json` na raiz do projeto downloader_PDSI
9. Na primeira execução, navegador abrirá para autenticação
10. Autorizar acesso ao Google Drive

**IMPORTANTE:** Consulte o arquivo [SETUP.md](SETUP.md) para instruções detalhadas com screenshots e troubleshooting.

**Documentação oficial:** [Google Drive API - Python Quickstart](https://developers.google.com/drive/api/quickstart/python)

---

## Configuração do Sistema

Todas as configurações do usuário estão centralizadas no arquivo `config.py` na raiz do projeto.

### Parâmetros principais:

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `USE_BATCH_FILE` | bool | Se True, processa arquivo .txt; se False, processa URL única | False |
| `URL` | str | URL única a processar (quando USE_BATCH_FILE=False) | "" |
| `AUDIO_FORMAT` | str | Formato do áudio (mp3, flac, wav, m4a, opus, ogg, aac) | "mp3" |
| `AUDIO_QUALITY` | int/str | Qualidade em kbps (0, 128, 192, 256, 320, "best") | 320 |
| `MIN_DURATION` | int | Duração mínima em segundos (filtro) | 150 |
| `MAX_DURATION` | int | Duração máxima em segundos (filtro) | 10000 |
| `DELAY_MIN` | int | Delay mínimo entre downloads em segundos | 6 |
| `DELAY_MAX` | int | Delay máximo entre downloads em segundos | 14 |
| `NOME_PASTA_DESTINO` | str | Nome da pasta no Drive dentro de BD_PDSI/ | "audios_katube" |

### Exemplos de configuração:

**Caso 1: Playlist completa com qualidade máxima**
```python
USE_BATCH_FILE = False
URL = "https://www.youtube.com/playlist?list=PLxxxxxxxxxxx"
AUDIO_FORMAT = "mp3"
AUDIO_QUALITY = "best"
MIN_DURATION = 60
MAX_DURATION = 3600
DELAY_MIN = 8
DELAY_MAX = 15
NOME_PASTA_DESTINO = "playlist_educacional"
```

**Caso 2: Múltiplos canais com filtros específicos**
```python
USE_BATCH_FILE = True  # Usa arquivo input/links.txt
AUDIO_FORMAT = "flac"
AUDIO_QUALITY = 0  # Melhor qualidade disponível
MIN_DURATION = 300   # Mínimo 5 minutos
MAX_DURATION = 7200  # Máximo 2 horas
DELAY_MIN = 10
DELAY_MAX = 20
NOME_PASTA_DESTINO = "pesquisa_audio_2024"
```

**Caso 3: Vídeo único para teste**
```python
USE_BATCH_FILE = False
URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
AUDIO_FORMAT = "mp3"
AUDIO_QUALITY = 192
MIN_DURATION = 0
MAX_DURATION = 1000
DELAY_MIN = 5
DELAY_MAX = 10
NOME_PASTA_DESTINO = "testes"
```

---

## Como Usar

### Modo 1: Link Único

Ideal para processar um vídeo, playlist ou canal específico.

**Passo 1:** Editar `config.py`
```python
USE_BATCH_FILE = False
URL = "https://www.youtube.com/playlist?list=PLxxxxxxxxxxx"
# Configurar demais parâmetros conforme necessário
```

**Passo 2:** Executar o sistema
```bash
python main.py
```

O sistema irá:
1. Validar configurações
2. Autenticar no Google Drive (primeira vez: abrirá navegador)
3. Detectar tipo de URL (vídeo, playlist ou canal)
4. Extrair IDs de todos os vídeos
5. Para cada vídeo:
   - Verificar se já foi processado (skip)
   - Baixar áudio localmente em temp/
   - Extrair metadados completos
   - Criar pasta no Drive: BD_PDSI/{NOME_PASTA_DESTINO}/{video_id}/
   - Upload de áudio e JSON
   - Limpar arquivo temporário
6. Consolidar CSV de metadados
7. Exibir estatísticas finais

### Modo 2: Batch de Links

Ideal para processar múltiplos vídeos, playlists e/ou canais em uma única execução.

**Passo 1:** Criar arquivo `input/links.txt`

Coloque um link por linha. Linhas vazias e comentários (iniciando com `#`) são ignorados.

```text
# Playlist 1: Curso de Python
https://www.youtube.com/playlist?list=PLxxxxxxxxx1

# Playlist 2: Palestras 2024
https://www.youtube.com/playlist?list=PLxxxxxxxxx2

# Canal completo
https://www.youtube.com/@nome_do_canal

# Vídeo individual importante
https://www.youtube.com/watch?v=xxxxxxxxxxx
```

**Passo 2:** Editar `config.py`
```python
USE_BATCH_FILE = True
# Configurar demais parâmetros conforme necessário
```

**Passo 3:** Executar o sistema
```bash
python main.py
```

O sistema processará todos os links sequencialmente, aplicando delays entre downloads.

---

## Estrutura de Arquivos

```
downloader_PDSI/
├── config.py                 # Configuracoes do usuario
├── main.py                   # Script principal (orquestrador)
├── requirements.txt          # Dependencias do projeto
├── credentials.json          # Credenciais OAuth2 Google (nao versionado)
├── token.pickle             # Token de acesso OAuth2 (nao versionado)
│
├── input/                   # Arquivos .txt com batch de links
│   ├── .gitkeep
│   └── links.txt            # Seu arquivo de links (nao versionado)
│
├── temp/                    # Downloads temporarios (nao versionado)
│   └── {video_id}/          # Pasta temporaria por video
│       ├── {video_id}.mp3
│       └── {video_id}.json
│
├── logs/                    # Logs persistentes (nao versionado)
│   ├── downloaded_ids.json  # IDs ja processados (sistema de skip)
│   ├── processing.log       # Log detalhado de execucao
│   └── errors.log           # Log de erros e problemas
│
└── src/                     # Modulos Python do sistema
    ├── config_validator.py  # Validacao de configuracoes
    ├── youtube_downloader.py # Core de download com yt-dlp
    ├── metadata_manager.py  # Gerenciamento de metadados CSV/JSON
    ├── drive_manager.py     # Integracao com Google Drive API
    └── utils.py             # Funcoes auxiliares e logging
```

---

## Estrutura no Google Drive

O sistema cria automaticamente a seguinte estrutura no seu Google Drive:

```
Google Drive (raiz)
└── BD_PDSI/
    └── {NOME_PASTA_DESTINO}/        # Ex: "audios_katube"
        ├── metadata.csv              # CSV consolidado com todos os metadados
        │
        ├── video_id_1/               # Pasta do primeiro video
        │   ├── video_id_1.mp3        # Audio do video
        │   └── video_id_1.json       # Metadados completos do video
        │
        ├── video_id_2/               # Pasta do segundo video
        │   ├── video_id_2.mp3
        │   └── video_id_2.json
        │
        └── video_id_N/               # Pasta do N-esimo video
            ├── video_id_N.mp3
            └── video_id_N.json
```

**Observações:**
- `BD_PDSI` é criado na raiz do Drive (uma única vez)
- `{NOME_PASTA_DESTINO}` é definido em `config.py`
- Cada vídeo tem sua própria pasta com áudio + metadados
- `metadata.csv` consolida metadados de todos os vídeos processados

---

## Metadados

O sistema extrai e salva metadados completos de cada vídeo em dois formatos:

### 1. CSV Consolidado (metadata.csv)

Arquivo CSV único com todos os vídeos processados.

**Formato:**
- **Separador:** Pipe (`|`) - evita conflitos com vírgulas em títulos
- **Encoding:** UTF-8 com BOM
- **Sanitização:** Automática de pipes, newlines e caracteres especiais

**Campos (9 colunas):**

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `id` | ID único do vídeo no YouTube | dQw4w9WgXcQ |
| `title` | Título do vídeo (sanitizado) | Never Gonna Give You Up |
| `duration` | Duração em segundos | 212 |
| `upload_date` | Data de upload (YYYYMMDD) | 20091025 |
| `uploader` | Nome do canal/uploader | Rick Astley |
| `uploader_id` | ID do canal | @RickAstleyYT |
| `view_count` | Número de visualizações | 1234567890 |
| `like_count` | Número de likes | 12345678 |
| `comment_count` | Número de comentários | 123456 |

**Exemplo de linha:**
```
dQw4w9WgXcQ|Never Gonna Give You Up|212|20091025|Rick Astley|@RickAstleyYT|1234567890|12345678|123456
```

### 2. JSON Individual

Um arquivo JSON por vídeo contendo metadados completos extraídos pelo yt-dlp.

**Localização:** `{video_id}/{video_id}.json`

**Campos incluídos:**
- Todos os 9 campos do CSV
- Campos adicionais: description, tags, categories, thumbnail, subtitles, etc.
- Backup completo de todos os metadados disponíveis

**Exemplo:**
```json
{
  "id": "dQw4w9WgXcQ",
  "title": "Never Gonna Give You Up",
  "duration": 212,
  "upload_date": "20091025",
  "uploader": "Rick Astley",
  "uploader_id": "@RickAstleyYT",
  "view_count": 1234567890,
  "like_count": 12345678,
  "comment_count": 123456,
  "description": "Official video...",
  "tags": ["music", "80s", "pop"],
  "thumbnail": "https://...",
  ...
}
```

---

## Logs

O sistema mantém três tipos de logs persistentes na pasta `logs/`:

### 1. downloaded_ids.json

Rastreia IDs de vídeos já processados para evitar reprocessamento.

**Estrutura:**
```json
{
  "downloaded_ids": [
    "dQw4w9WgXcQ",
    "jNQXAC9IVRw",
    "oHg5SJYRHA0"
  ],
  "last_updated": "2024-01-15T14:30:00"
}
```

**Funcionalidade:**
- ID adicionado após upload bem-sucedido para o Drive
- Sistema verifica este arquivo antes de processar cada vídeo
- Se ID já existe: skip (não reprocessa)
- Permite retomar execuções interrompidas sem reprocessar

### 2. processing.log

Log detalhado de todas as operações realizadas.

**Formato:** `[YYYY-MM-DD HH:MM:SS] LEVEL: Mensagem`

**Registra:**
- Início e fim de execução
- Configurações carregadas
- URLs detectadas e IDs extraídos
- Downloads iniciados e concluídos
- Uploads realizados
- Vídeos pulados (skip)
- Estatísticas finais

**Exemplo:**
```
[2024-01-15 14:30:00] INFO: ======================================================================
[2024-01-15 14:30:00] INFO: Iniciando execucao do Downloader PDSI
[2024-01-15 14:30:01] INFO: Modo: URL_UNICA
[2024-01-15 14:30:02] INFO: URL detectada como: PLAYLIST
[2024-01-15 14:30:03] INFO: Total de videos extraidos: 25
[2024-01-15 14:30:05] INFO: Processando video 1/25: dQw4w9WgXcQ
[2024-01-15 14:30:25] INFO: Download concluido: dQw4w9WgXcQ
[2024-01-15 14:30:40] INFO: Upload concluido: dQw4w9WgXcQ
```

### 3. errors.log

Log exclusivo de erros e problemas encontrados.

**Registra:**
- Vídeos indisponíveis ou privados
- Falhas de download após todas as tentativas de retry
- Falhas de upload após todas as tentativas de retry
- Erros de rede
- Problemas de autenticação

**Exemplo:**
```
[2024-01-15 14:32:10] ERROR: Falha no download do video xyz123 apos 2 tentativas
[2024-01-15 14:35:20] ERROR: Video abc456 indisponivel: Private video
```

---

## Troubleshooting

### Problema 1: "credentials.json not found"

**Sintoma:** Erro ao iniciar o sistema informando que arquivo não foi encontrado.

**Causa:** Arquivo `credentials.json` não está presente na raiz do projeto.

**Solução:**
1. Verificar se arquivo `credentials.json` existe na raiz do projeto
2. Se não existe, seguir guia de configuração: [SETUP.md](SETUP.md)
3. Baixar credentials.json do Google Cloud Console
4. Colocar na raiz do projeto (mesmo nível que main.py)

---

### Problema 2: "Access blocked: This app's request is invalid"

**Sintoma:** Erro durante autenticação OAuth2 no navegador.

**Causa:** Tela de consentimento OAuth2 não está configurada corretamente ou usuário não está adicionado como teste.

**Solução:**
1. Acessar [Google Cloud Console](https://console.cloud.google.com/)
2. Selecionar seu projeto
3. Ir em "APIs & Services" > "OAuth consent screen"
4. Verificar se tela de consentimento está publicada ou em modo teste
5. Se em modo teste: adicionar seu email em "Test users"
6. Salvar alterações
7. Deletar `token.pickle` se existir
8. Executar `python main.py` novamente

---

### Problema 3: "Video unavailable"

**Sintoma:** Mensagem indicando que vídeo está indisponível durante processamento.

**Causa:** Vídeo é privado, foi removido, ou está com restrições geográficas.

**Solução:**
- Este é um comportamento normal
- Sistema pula automaticamente vídeos indisponíveis
- Erro registrado em `logs/errors.log`
- Processamento continua com próximos vídeos
- Verificar se vídeo realmente existe e é público

---

### Problema 4: "Rate limit exceeded" ou muitos erros 429

**Sintoma:** Múltiplos erros de rate limiting do YouTube.

**Causa:** Delays entre downloads muito curtos, muitas requisições em curto período.

**Solução:**
1. Editar `config.py`
2. Aumentar `DELAY_MIN` e `DELAY_MAX`:
   ```python
   DELAY_MIN = 15  # Era 6
   DELAY_MAX = 25  # Era 14
   ```
3. Executar novamente
4. Sistema de skip evitará reprocessar vídeos já baixados

---

### Problema 5: Token expirado ou inválido

**Sintoma:** Erro de autenticação ao tentar acessar Google Drive.

**Causa:** Token de acesso (`token.pickle`) expirou ou foi invalidado.

**Solução:**
1. Deletar arquivo `token.pickle` da raiz do projeto:
   ```bash
   rm token.pickle
   ```
2. Executar `python main.py` novamente
3. Sistema abrirá navegador para reautenticação
4. Autorizar acesso novamente
5. Novo token será gerado automaticamente

---

### Problema 6: "Insufficient storage" no Google Drive

**Sintoma:** Erro ao fazer upload indicando falta de espaço.

**Causa:** Conta Google Drive sem espaço disponível.

**Solução:**
1. Verificar espaço disponível no Drive: https://drive.google.com/
2. Liberar espaço deletando arquivos desnecessários
3. Considerar upgrade de plano do Google One
4. Após liberar espaço, executar novamente
5. Sistema tentará apenas vídeos que falharam (via skip)

---

### Problema 7: Erros de permissão ao criar diretórios

**Sintoma:** Erro de permissão ao tentar criar `temp/` ou `logs/`.

**Causa:** Usuário sem permissões de escrita no diretório do projeto.

**Solução:**
- **Linux/macOS:**
  ```bash
  chmod -R u+w downloader_PDSI/
  ```
- **Windows:** Verificar propriedades da pasta e permissões de escrita

---

## Limitações Conhecidas

1. **Taxa de download do YouTube:** O YouTube implementa rate limiting. Use delays apropriados (recomendado: 8-15 segundos).

2. **Vídeos privados/removidos:** Não podem ser baixados. Sistema pula automaticamente.

3. **Reautenticação OAuth2:** Token pode expirar após períodos longos de inatividade. Reautenticação é simples (deletar token.pickle e executar novamente).

4. **Modo "Teste" OAuth2:** Limite de 100 usuários de teste. Para uso público, necessário publicar app (processo de verificação Google).

5. **Vídeos com restrição geográfica:** Podem não estar disponíveis dependendo da localização.

6. **Playlists muito grandes:** Processamento pode levar horas. Sistema permite retomar via skip.

7. **Metadados de vídeos ao vivo:** Alguns campos podem estar indisponíveis durante transmissões ao vivo.

---

## Boas Práticas

### Durante Uso:

1. **Use delays apropriados:** Não reduza DELAY_MIN abaixo de 5 segundos para evitar rate limiting

2. **Monitore logs regularmente:** Verifique `logs/errors.log` para identificar problemas recorrentes

3. **Faça backup de downloaded_ids.json:** Evita reprocessamento desnecessário em caso de perda

4. **Teste com poucos vídeos primeiro:** Antes de processar playlists grandes, teste configuração com 2-3 vídeos

5. **Mantenha credentials.json seguro:** Nunca compartilhe este arquivo ou faça commit no git

### Manutenção:

6. **Limpe temp/ periodicamente:** Em caso de falhas, arquivos podem acumular (sistema limpa automaticamente ao iniciar)

7. **Atualize dependências:** Execute periodicamente:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

8. **Verifique espaço no Drive:** Monitore uso de espaço antes de processar grandes volumes

9. **Revise .gitignore antes de commits:** Garanta que credentials.json e token.pickle não sejam versionados

### Configuração OAuth2:

10. **Use escopo mínimo:** Sistema usa apenas `https://www.googleapis.com/auth/drive.file` (acesso apenas a arquivos criados pelo app)

11. **Adicione apenas usuários necessários:** Em modo teste, adicione apenas emails que realmente usarão o sistema

---

## Segurança

### Arquivos Sensíveis:

**credentials.json**
- Contém `client_id` e `client_secret` da aplicação OAuth2
- NUNCA compartilhar publicamente
- NUNCA fazer commit em repositórios (já está no .gitignore)

**token.pickle**
- Contém token de acesso OAuth2 com permissões ao seu Google Drive
- NUNCA compartilhar publicamente
- NUNCA fazer commit em repositórios (já está no .gitignore)
- Permite acesso ao Drive sem senha, tratar como credencial sensível

### Boas Práticas de Segurança:

1. **Verifique .gitignore:** Antes de qualquer commit, confirme que arquivos sensíveis estão listados

2. **Use escopo mínimo:** Sistema solicita apenas permissão `drive.file`, não acesso total ao Drive

3. **Revogue acesso se comprometido:** Se credentials.json ou token.pickle vazarem:
   - Acesse [Google Account - Apps with access](https://myaccount.google.com/permissions)
   - Remova acesso do app "Downloader PDSI"
   - Delete token.pickle
   - Gere novas credenciais no Cloud Console

4. **Não use em ambientes compartilhados:** Evite executar em servidores públicos ou computadores compartilhados

5. **Atenção ao compartilhar screenshots:** Oculte `client_id` e `client_secret` se compartilhar telas do Cloud Console

---

## Contribuindo

Contribuições são bem-vindas! Siga as diretrizes abaixo:

### Reportar Bugs:

1. Abra uma issue no [GitHub Issues](https://github.com/DosAnjos-AI/downloader_PDSI/issues)
2. Descreva o problema detalhadamente
3. Inclua passos para reproduzir
4. Anexe logs relevantes (remova informações sensíveis)
5. Especifique versão do Python e sistema operacional

### Sugerir Melhorias:

1. Abra uma issue com tag `enhancement`
2. Descreva a funcionalidade desejada
3. Explique o caso de uso
4. Se possível, sugira implementação

### Enviar Pull Requests:

1. Fork o repositório
2. Crie branch para sua feature: `git checkout -b feature/nome-da-feature`
3. Siga padrões de código do projeto:
   - Comentários em português sem emojis
   - Type hints em todas as funções
   - Docstrings descritivas
   - Tratamento de exceções robusto
4. Teste suas mudanças completamente
5. Commit com mensagens descritivas em português
6. Push para seu fork
7. Abra Pull Request detalhando mudanças

### Padrões de Código:

- **Linguagem:** Python 3.8+
- **Estilo:** PEP 8
- **Comentários:** Português, sem emojis
- **Docstrings:** Formato Google/NumPy
- **Type hints:** Obrigatório
- **Testes:** Validação manual de todas as features

---

## Licença

Este projeto está licenciado sob a **MIT License**.

Veja o arquivo [LICENSE](LICENSE) para detalhes completos.

### Resumo da Licença MIT:

Você é livre para:
- Usar comercialmente
- Modificar
- Distribuir
- Uso privado

Sob as condições:
- Incluir aviso de copyright
- Incluir cópia da licença

Sem garantias de qualquer tipo.

---

## Autores

**Projeto:** Downloader PDSI
**Desenvolvedor:** DosAnjos-AI
**Repositório:** [github.com/DosAnjos-AI/downloader_PDSI](https://github.com/DosAnjos-AI/downloader_PDSI)

### Contato:

- **GitHub:** [@DosAnjos-AI](https://github.com/DosAnjos-AI)
- **Issues:** [GitHub Issues](https://github.com/DosAnjos-AI/downloader_PDSI/issues)

---

## Referências

### Tecnologias e Bibliotecas:

- **yt-dlp:** [github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
  - Fork do youtube-dl com features adicionais e manutenção ativa
  - Documentação: [github.com/yt-dlp/yt-dlp#readme](https://github.com/yt-dlp/yt-dlp#readme)

- **Google Drive API:** [developers.google.com/drive/api](https://developers.google.com/drive/api)
  - API oficial do Google Drive para integração programática
  - Python Quickstart: [developers.google.com/drive/api/quickstart/python](https://developers.google.com/drive/api/quickstart/python)

- **Python Google API Client:** [github.com/googleapis/google-api-python-client](https://github.com/googleapis/google-api-python-client)
  - Cliente oficial Python para APIs do Google

- **pandas:** [pandas.pydata.org](https://pandas.pydata.org)
  - Biblioteca de análise e manipulação de dados

### Projetos Relacionados:

- **katube-colab:** [github.com/DosAnjos-AI/katube-colab](https://github.com/DosAnjos-AI/katube-colab)
  - Versão original para Google Colab
  - downloader_PDSI é adaptação standalone para uso local

### Documentação Adicional:

- **OAuth 2.0:** [developers.google.com/identity/protocols/oauth2](https://developers.google.com/identity/protocols/oauth2)
- **Google Cloud Console:** [console.cloud.google.com](https://console.cloud.google.com)
- **YouTube Data API:** [developers.google.com/youtube/v3](https://developers.google.com/youtube/v3)

---

## Agradecimentos

Agradecimentos especiais a:
- Comunidade **yt-dlp** pelo excelente trabalho de manutenção
- Google pela disponibilização da Drive API
- Comunidade Python pelo ecossistema rico de bibliotecas
- Todos os contribuidores e usuários do projeto

---

**Versão:** 1.0
**Última atualização:** 2024-01-15
**Status:** Estável
