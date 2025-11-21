"""
Funções utilitárias do Downloader Local PDSI.
"""

import re
import random
import time
from pathlib import Path
from typing import Optional, Tuple


def detect_url_type(url: str) -> str:
    """
    Detecta o tipo de URL do YouTube.
    
    Args:
        url: URL do YouTube
        
    Returns:
        Tipo da URL: "video", "playlist" ou "channel"
        
    Raises:
        ValueError: Se URL for inválida ou não reconhecida
    """
    url = url.strip()
    
    # Validar se é URL do YouTube
    if not re.search(r'(youtube\.com|youtu\.be)', url):
        raise ValueError(f"URL inválida: não é do YouTube - {url}")
    
    # Detectar playlist
    if 'list=' in url:
        return "playlist"
    
    # Detectar canal
    if re.search(r'/@[\w-]+(/videos)?', url) or '/channel/' in url or '/c/' in url:
        return "channel"
    
    # Detectar vídeo único
    if re.search(r'(watch\?v=|youtu\.be/)', url):
        return "video"
    
    raise ValueError(f"Tipo de URL não reconhecido: {url}")


def extract_source_id(url: str, url_type: str) -> str:
    """
    Extrai o ID da fonte (playlist, canal ou vídeo) da URL.
    
    Args:
        url: URL do YouTube
        url_type: Tipo da URL ("video", "playlist" ou "channel")
        
    Returns:
        ID da fonte extraído
        
    Raises:
        ValueError: Se não conseguir extrair ID
    """
    if url_type == "playlist":
        match = re.search(r'list=([\w-]+)', url)
        if match:
            return f"playlist_{match.group(1)}"
    
    elif url_type == "channel":
        # Tentar extrair @username
        match = re.search(r'/@([\w-]+)', url)
        if match:
            return f"channel_{match.group(1)}"
        
        # Tentar extrair ID do canal
        match = re.search(r'/channel/([\w-]+)', url)
        if match:
            return f"channel_{match.group(1)}"
        
        # Tentar extrair custom URL
        match = re.search(r'/c/([\w-]+)', url)
        if match:
            return f"channel_{match.group(1)}"
    
    elif url_type == "video":
        # URL padrão
        match = re.search(r'watch\?v=([\w-]+)', url)
        if match:
            return f"video_{match.group(1)}"
        
        # URL encurtada
        match = re.search(r'youtu\.be/([\w-]+)', url)
        if match:
            return f"video_{match.group(1)}"
    
    raise ValueError(f"Não foi possível extrair ID da URL: {url}")


def sanitize_string(text: str) -> str:
    """
    Sanitiza string para uso em CSV e nomes de arquivo.
    
    Remove:
    - Quebras de linha (\n, \r, \r\n)
    - Pipes (|) - substituídos por hífen
    - Espaços duplicados
    - Caracteres de controle
    
    Args:
        text: String a ser sanitizada
        
    Returns:
        String sanitizada
    """
    if not text:
        return ""
    
    # Remover quebras de linha
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    # Substituir pipes por hífen
    text = text.replace('|', '-')
    
    # Remover espaços duplicados
    text = re.sub(r'\s+', ' ', text)
    
    # Remover caracteres de controle
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\t')
    
    return text.strip()


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitiza string para uso como nome de arquivo.
    
    Remove caracteres inválidos para sistemas de arquivo Windows/Linux.
    
    Args:
        filename: Nome do arquivo
        max_length: Comprimento máximo do nome
        
    Returns:
        Nome de arquivo sanitizado
    """
    # Remover caracteres inválidos para Windows e Linux
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    filename = re.sub(invalid_chars, '_', filename)
    
    # Remover espaços duplicados
    filename = re.sub(r'\s+', ' ', filename)
    
    # Limitar comprimento
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        name = name[:max_length - len(ext) - 1]
        filename = f"{name}.{ext}" if ext else name
    
    return filename.strip()


def random_delay(min_seconds: int, max_seconds: int) -> int:
    """
    Gera delay randômico e executa sleep.
    
    Args:
        min_seconds: Delay mínimo em segundos
        max_seconds: Delay máximo em segundos
        
    Returns:
        Número de segundos sorteados
    """
    delay = random.randint(min_seconds, max_seconds)
    time.sleep(delay)
    return delay


def ensure_dir(path: Path) -> Path:
    """
    Garante que diretório existe, criando se necessário.
    
    Args:
        path: Caminho do diretório
        
    Returns:
        Path do diretório criado
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_base_dir() -> Path:
    """
    Retorna o diretório raiz do projeto.
    
    Returns:
        Path do diretório raiz
    """
    # Assumindo que utils.py está em src/
    return Path(__file__).parent.parent


def format_duration(seconds: int) -> str:
    """
    Formata duração em segundos para formato legível.
    
    Args:
        seconds: Duração em segundos
        
    Returns:
        String formatada (ex: "2h 30m 45s" ou "3m 20s")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"
