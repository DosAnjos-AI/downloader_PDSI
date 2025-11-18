"""
Modulo de funcoes utilitarias para o downloader_PDSI.
Contem funcoes auxiliares para sanitizacao de texto e geracao de delays.
"""

import re
import random


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
