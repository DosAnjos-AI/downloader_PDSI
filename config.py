"""
Configurações centralizadas do Downloader Local PDSI.
Todos os parâmetros são ajustáveis pelo usuário.
"""

# ==============================================================================
# MODO DE OPERAÇÃO
# ==============================================================================

# Define se processa arquivo de batch ou URL única
# True: Lê arquivo .txt da pasta input/
# False: Processa URL definida abaixo
USE_BATCH_FILE = False

# ==============================================================================
# INPUT - LINK ÚNICO (usado se USE_BATCH_FILE = False)
# ==============================================================================

# URL do YouTube (vídeo, playlist ou canal)
# Exemplos:
#   Vídeo:    "https://www.youtube.com/watch?v=VIDEO_ID"
#   Playlist: "https://www.youtube.com/playlist?list=PLAYLIST_ID"
#   Canal:    "https://www.youtube.com/@CHANNEL_NAME/videos"
URL = "https://www.youtube.com/watch?v=VIDEO_ID"

# ==============================================================================
# OUTPUT - NOMENCLATURA
# ==============================================================================

# Nome da pasta de saída em output/
# "default": Usa automaticamente o source_ID (playlist_ID, channel_ID ou video_ID)
# Qualquer string: Cria pasta com o nome especificado
# Exemplo: "minha_colecao" → output/minha_colecao/
NOME_PASTA_OUTPUT = "default"

# ==============================================================================
# CONFIGURAÇÕES DE ÁUDIO
# ==============================================================================

# Formato do áudio final
# Opções: "mp3", "flac", "wav", "m4a", "ogg", "opus"
# Recomendado: "mp3" (melhor compatibilidade)
AUDIO_FORMAT = "mp3"

# Qualidade do áudio em kbps
# Opções:
#   320: Qualidade máxima para MP3
#   256: Alta qualidade (ótimo custo-benefício)
#   192: Boa qualidade, arquivo menor
#   128: Qualidade básica
#   0 ou "best": Máxima qualidade disponível
AUDIO_QUALITY = 320

# ==============================================================================
# FILTROS DE DURAÇÃO
# ==============================================================================

# Duração mínima do vídeo em segundos
# Vídeos com duração menor que este valor serão pulados (skip)
# Exemplo: 150 = 2min 30s
MIN_DURATION = 150

# Duração máxima do vídeo em segundos
# Vídeos com duração maior que este valor serão pulados (skip)
# Exemplo: 10000 = 2h 46min 40s
MAX_DURATION = 10000

# ==============================================================================
# SEGMENTAÇÃO DE ÁUDIO
# ==============================================================================

# Duração do segmento em segundos (primeiros X segundos do áudio)
# O sistema cortará apenas o início do áudio
# Restante será descartado após normalização
# Exemplo: 150 = primeiros 2min 30s
# Nota: Vídeos com duração < SEGMENT_DURATION serão pulados
SEGMENT_DURATION = 150

# ==============================================================================
# NORMALIZAÇÃO DE ÁUDIO (SOX)
# ==============================================================================

# Nível alvo de normalização em decibéis (dB)
# Valores negativos reduzem o volume de pico
# Valores típicos:
#   -3.0: Padrão para datasets de IA (recomendado)
#   -1.0: Quase no limite
#   0.0: Volume máximo (pode causar clipping)
NORMALIZE_TARGET = -3.0

# Converter áudio de stereo para mono
# True: Converte para mono (recomendado para TTS/IA)
# False: Mantém stereo se disponível
CONVERT_TO_MONO = True

# Taxa de amostragem alvo em Hz (sample rate)
# Valores comuns:
#   22050: Padrão para datasets de TTS
#   16000: Usado em reconhecimento de fala
#   44100: CD quality
#   48000: Professional audio
TARGET_SAMPLE_RATE = 22050

# ==============================================================================
# DELAY RANDÔMICO
# ==============================================================================

# Delay mínimo entre chamadas do yt-dlp em segundos
# Evita sobrecarga e possíveis bloqueios do YouTube
DELAY_MIN = 6

# Delay máximo entre chamadas do yt-dlp em segundos
# Um valor aleatório entre MIN e MAX será sorteado a cada download
DELAY_MAX = 14

# ==============================================================================
# FILTROS DE CONTEÚDO
# ==============================================================================

# Pular YouTube Shorts (vídeos < 60s)
# True: Ignora Shorts automaticamente
# False: Processa normalmente (respeitando MIN_DURATION)
SKIP_SHORTS = True

# ==============================================================================
# LIMPEZA E MANUTENÇÃO
# ==============================================================================

# Deletar pasta temp/ após processamento bem-sucedido
# True: Limpa automaticamente (recomendado)
# False: Mantém arquivos temporários (útil para debug)
AUTO_CLEANUP_TEMP = True

# Manter áudio original não-processado em output/
# True: Salva original.mp3 + processado.mp3
# False: Salva apenas o áudio final normalizado (recomendado)
KEEP_ORIGINAL_AUDIO = False

# ==============================================================================
# RETRY E TIMEOUT
# ==============================================================================

# Número de tentativas adicionais em caso de falha no download
# 0: Sem retry, pula imediatamente
# 1: Tenta mais uma vez antes de pular (recomendado)
# 2+: Múltiplas tentativas (pode aumentar tempo total)
RETRY_ATTEMPTS = 1

# Timeout para cada download em segundos
# Após este tempo sem resposta, o download é cancelado
# Exemplo: 300 = 5 minutos
TIMEOUT_SECONDS = 300
