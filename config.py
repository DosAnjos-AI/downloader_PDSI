# Configuracoes do downloader_PDSI
# Sistema local de download de audios do YouTube com upload automatico para Google Drive

# ==============================================================================
# MODO DE OPERACAO
# ==============================================================================
# False: Baixar apenas uma URL (definida em URL abaixo)
# True: Processar arquivo batch com multiplas URLs (arquivo .txt na pasta input/)
USE_BATCH_FILE = False

# ==============================================================================
# INPUT - LINK UNICO
# ==============================================================================
# URL do video quando USE_BATCH_FILE = False
# Exemplo: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
URL = "https://www.youtube.com/watch?v=VIDEO_ID"

# ==============================================================================
# BATCH FILE - MULTIPLOS LINKS
# ==============================================================================
# Quando USE_BATCH_FILE = True, colocar arquivo .txt na pasta input/
# Formato do arquivo:
#   - Um link por linha
#   - Sem cabecalhos
#   - Sem linhas vazias entre os links
#
# Exemplo de conteudo do arquivo input/links.txt:
#   https://www.youtube.com/watch?v=VIDEO_ID1
#   https://www.youtube.com/watch?v=VIDEO_ID2
#   https://www.youtube.com/watch?v=VIDEO_ID3

# ==============================================================================
# CONFIGURACOES DE AUDIO
# ==============================================================================
# Formato de saida do audio
# Opcoes disponiveis: mp3, flac, wav, m4a, ogg, opus
AUDIO_FORMAT = "mp3"

# Qualidade do audio em kbps
# Opcoes: 0 ou "best" (melhor qualidade), 320, 256, 192, 128
# Recomendado: 320 para maxima qualidade em MP3
AUDIO_QUALITY = 320

# Duracao minima do video em segundos (videos mais curtos serao ignorados)
# 150 segundos = 2 minutos e 30 segundos
MIN_DURATION = 150

# Duracao maxima do video em segundos (videos mais longos serao ignorados)
# 10000 segundos = 2 horas, 46 minutos e 40 segundos
MAX_DURATION = 10000

# ==============================================================================
# DELAY RANDOMICO ENTRE DOWNLOADS
# ==============================================================================
# Intervalo aleatorio entre downloads para evitar bloqueio
# O sistema aguardara um tempo aleatorio entre DELAY_MIN e DELAY_MAX segundos
DELAY_MIN = 6
DELAY_MAX = 14

# ==============================================================================
# GOOGLE DRIVE - CONFIGURACOES DE UPLOAD
# ==============================================================================
# Nome da pasta de destino no Google Drive
# Estrutura final: BD_PDSI/NOME_PASTA_DESTINO/video_ID/
#
# Exemplo com NOME_PASTA_DESTINO = "audios_katube":
#   BD_PDSI/
#       audios_katube/
#           dQw4w9WgXcQ/
#               audio.mp3
#               metadata.json
#           AbCdEfGhIjK/
#               audio.mp3
#               metadata.json
#
# A pasta BD_PDSI sera criada automaticamente na raiz do Drive
# Cada video tera uma subpasta com seu ID unico
NOME_PASTA_DESTINO = "audios_katube"
