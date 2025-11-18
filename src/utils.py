"""
Modulo de funcoes utilitarias para o downloader_PDSI.
Contem funcoes auxiliares para sanitizacao de texto, geracao de delays,
gerenciamento de IDs processados e configuracao de logging.
"""

import re
import random
import json
import logging
from pathlib import Path
from datetime import datetime


def sanitize_filename(text: str) -> str:
    """
    Remove caracteres invalidos para nomes de arquivo.

    Remove ou substitui caracteres especiais que nao sao permitidos
    em nomes de arquivo em diferentes sistemas operacionais.
    Mantem apenas letras, numeros, espacos, hifens e underscores.

    Args:
        text: Texto a ser sanitizado

    Returns:
        str: Texto limpo e seguro para usar como nome de arquivo

    Exemplo:
        >>> sanitize_filename("video|name<test>file\n.mp3")
        "videonametestfile.mp3"
    """
    if not text:
        return ""

    # Remove quebras de linha
    text = text.replace('\n', '').replace('\r', '').replace('\r\n', '')

    # Remove pipes
    text = text.replace('|', '')

    # Remove caracteres especiais invalidos para nomes de arquivo
    # Mantem apenas: letras, numeros, espacos, hifens, underscores e pontos
    text = re.sub(r'[<>:"/\\|?*]', '', text)

    # Remove espacos duplicados
    text = re.sub(r'\s+', ' ', text)

    # Remove espacos no inicio e fim
    text = text.strip()

    return text


def sanitize_metadata_field(text: str) -> str:
    """
    Sanitiza campos de metadata para armazenamento seguro.

    Remove quebras de linha, substitui pipes por hifens e
    limpa espacos duplicados.

    Args:
        text: Texto a ser sanitizado

    Returns:
        str: Texto limpo e seguro para metadata

    Exemplo:
        >>> sanitize_metadata_field("text|with\npipes\rand  spaces")
        "text-with pipes and spaces"
    """
    if not text:
        return ""

    # Remove quebras de linha
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\r\n', ' ')

    # Substitui pipes por hifens
    text = text.replace('|', '-')

    # Remove espacos duplicados
    text = re.sub(r'\s+', ' ', text)

    # Remove espacos no inicio e fim
    text = text.strip()

    return text


def random_delay(min_seconds: int, max_seconds: int) -> int:
    """
    Gera um delay randomico entre min e max segundos.

    Util para evitar bloqueios por requisicoes muito frequentes.

    Args:
        min_seconds: Tempo minimo em segundos
        max_seconds: Tempo maximo em segundos

    Returns:
        int: Numero aleatorio de segundos entre min_seconds e max_seconds (inclusive)

    Raises:
        ValueError: Se min_seconds > max_seconds

    Exemplo:
        >>> delay = random_delay(6, 14)
        >>> assert 6 <= delay <= 14
    """
    if min_seconds > max_seconds:
        raise ValueError(f"min_seconds ({min_seconds}) deve ser menor ou igual a max_seconds ({max_seconds})")

    return random.randint(min_seconds, max_seconds)


def load_downloaded_ids(log_path: Path) -> set[str]:
    """
    Carrega IDs de videos ja processados do arquivo de log.

    Le o arquivo downloaded_ids.json e retorna um set com todos os IDs
    ja processados. Se o arquivo nao existir, cria a estrutura inicial.

    Args:
        log_path: Caminho para o arquivo downloaded_ids.json

    Returns:
        set[str]: Set contendo IDs de videos ja processados

    Exemplo:
        >>> ids = load_downloaded_ids(Path('logs/downloaded_ids.json'))
        >>> 'abc123' in ids
        False
    """
    try:
        # Verifica se arquivo existe
        if not log_path.exists():
            # Cria estrutura inicial
            log_path.parent.mkdir(parents=True, exist_ok=True)
            initial_data = {
                "downloaded_ids": [],
                "last_updated": None
            }
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2)
            return set()

        # Carrega arquivo existente
        with open(log_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Retorna set de IDs
        return set(data.get('downloaded_ids', []))

    except json.JSONDecodeError:
        # Arquivo JSON corrompido, recria estrutura inicial
        initial_data = {
            "downloaded_ids": [],
            "last_updated": None
        }
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2)
        return set()
    except Exception as e:
        print(f"Erro ao carregar IDs baixados: {e}")
        return set()


def add_downloaded_id(video_id: str, log_path: Path) -> bool:
    """
    Adiciona ID de video processado ao arquivo de log.

    Adiciona o video_id a lista de IDs processados e atualiza o
    timestamp de ultima modificacao. Previne duplicatas.

    Args:
        video_id: ID do video do YouTube
        log_path: Caminho para o arquivo downloaded_ids.json

    Returns:
        bool: True se adicionado com sucesso, False caso contrario

    Exemplo:
        >>> add_downloaded_id('abc123', Path('logs/downloaded_ids.json'))
        True
    """
    try:
        # Carrega dados atuais
        if log_path.exists():
            with open(log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            # Cria estrutura inicial se nao existe
            log_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "downloaded_ids": [],
                "last_updated": None
            }

        # Adiciona ID se nao existe (previne duplicatas)
        if video_id not in data['downloaded_ids']:
            data['downloaded_ids'].append(video_id)

        # Atualiza timestamp
        data['last_updated'] = datetime.now().isoformat()

        # Salva arquivo
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Erro ao adicionar ID baixado: {e}")
        return False


def is_downloaded(video_id: str, downloaded_ids: set[str]) -> bool:
    """
    Verifica se video ja foi processado.

    Verifica se o video_id esta presente no set de IDs ja processados.

    Args:
        video_id: ID do video do YouTube
        downloaded_ids: Set com IDs de videos ja processados

    Returns:
        bool: True se ja foi processado, False caso contrario

    Exemplo:
        >>> ids = {'abc123', 'def456'}
        >>> is_downloaded('abc123', ids)
        True
        >>> is_downloaded('xyz999', ids)
        False
    """
    return video_id in downloaded_ids


def setup_logging(logs_dir: Path) -> tuple[logging.Logger, logging.Logger]:
    """
    Configura sistema de logging do projeto.

    Cria dois loggers separados:
    - processing_logger: registra INFO em logs/processing.log
    - error_logger: registra ERROR/WARNING em logs/errors.log

    Formato: [YYYY-MM-DD HH:MM:SS] LEVEL: Mensagem

    Args:
        logs_dir: Diretorio onde os arquivos de log serao salvos

    Returns:
        tuple[logging.Logger, logging.Logger]: (processing_logger, error_logger)

    Exemplo:
        >>> proc_log, err_log = setup_logging(Path('logs'))
        >>> proc_log.info('Processamento iniciado')
        >>> err_log.error('Erro detectado')
    """
    # Cria diretorio de logs se nao existe
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Define formato dos logs
    log_format = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')

    # Configura processing logger
    processing_logger = logging.getLogger('processing')
    processing_logger.setLevel(logging.INFO)
    processing_logger.handlers.clear()

    proc_handler = logging.FileHandler(logs_dir / 'processing.log', encoding='utf-8')
    proc_handler.setLevel(logging.INFO)
    proc_handler.setFormatter(log_format)
    processing_logger.addHandler(proc_handler)

    # Adiciona handler para console tambem
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    processing_logger.addHandler(console_handler)

    # Configura error logger
    error_logger = logging.getLogger('errors')
    error_logger.setLevel(logging.WARNING)
    error_logger.handlers.clear()

    err_handler = logging.FileHandler(logs_dir / 'errors.log', encoding='utf-8')
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(log_format)
    error_logger.addHandler(err_handler)

    return processing_logger, error_logger
