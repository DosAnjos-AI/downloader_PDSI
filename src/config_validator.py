"""
Modulo de validacao das configuracoes do downloader_PDSI.
Verifica se todas as variaveis obrigatorias existem e possuem valores validos.
"""

import sys
import os

# Adiciona o diretorio raiz ao path para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


def validate_config() -> bool:
    """
    Valida todas as configuracoes do arquivo config.py.

    Verifica:
    - Existencia de todas as variaveis obrigatorias
    - Tipos de dados corretos
    - Valores dentro de limites aceitaveis
    - Relacoes logicas entre variaveis (ex: MIN < MAX)

    Returns:
        bool: True se todas as validacoes passarem, False caso contrario
    """

    # Lista de variaveis obrigatorias
    required_vars = [
        'USE_BATCH_FILE',
        'URL',
        'AUDIO_FORMAT',
        'AUDIO_QUALITY',
        'MIN_DURATION',
        'MAX_DURATION',
        'DELAY_MIN',
        'DELAY_MAX',
        'NOME_PASTA_DESTINO'
    ]

    # Verificar existencia de todas as variaveis
    for var in required_vars:
        if not hasattr(config, var):
            print(f"ERRO: Variavel obrigatoria '{var}' nao encontrada em config.py")
            return False

    # Validar tipos de dados
    if not isinstance(config.USE_BATCH_FILE, bool):
        print(f"ERRO: USE_BATCH_FILE deve ser bool, encontrado: {type(config.USE_BATCH_FILE).__name__}")
        return False

    if not isinstance(config.URL, str):
        print(f"ERRO: URL deve ser str, encontrado: {type(config.URL).__name__}")
        return False

    if not isinstance(config.AUDIO_FORMAT, str):
        print(f"ERRO: AUDIO_FORMAT deve ser str, encontrado: {type(config.AUDIO_FORMAT).__name__}")
        return False

    if not isinstance(config.AUDIO_QUALITY, int):
        print(f"ERRO: AUDIO_QUALITY deve ser int, encontrado: {type(config.AUDIO_QUALITY).__name__}")
        return False

    if not isinstance(config.MIN_DURATION, int):
        print(f"ERRO: MIN_DURATION deve ser int, encontrado: {type(config.MIN_DURATION).__name__}")
        return False

    if not isinstance(config.MAX_DURATION, int):
        print(f"ERRO: MAX_DURATION deve ser int, encontrado: {type(config.MAX_DURATION).__name__}")
        return False

    if not isinstance(config.DELAY_MIN, int):
        print(f"ERRO: DELAY_MIN deve ser int, encontrado: {type(config.DELAY_MIN).__name__}")
        return False

    if not isinstance(config.DELAY_MAX, int):
        print(f"ERRO: DELAY_MAX deve ser int, encontrado: {type(config.DELAY_MAX).__name__}")
        return False

    if not isinstance(config.NOME_PASTA_DESTINO, str):
        print(f"ERRO: NOME_PASTA_DESTINO deve ser str, encontrado: {type(config.NOME_PASTA_DESTINO).__name__}")
        return False

    # Validar formato de audio
    valid_formats = ['mp3', 'flac', 'wav', 'm4a', 'ogg', 'opus']
    if config.AUDIO_FORMAT.lower() not in valid_formats:
        print(f"ERRO: AUDIO_FORMAT '{config.AUDIO_FORMAT}' invalido. Opcoes validas: {', '.join(valid_formats)}")
        return False

    # Validar qualidade de audio
    valid_qualities = [0, 128, 192, 256, 320]
    if config.AUDIO_QUALITY not in valid_qualities:
        print(f"ERRO: AUDIO_QUALITY {config.AUDIO_QUALITY} invalida. Opcoes validas: {', '.join(map(str, valid_qualities))} ou 'best'")
        return False

    # Validar duracao minima e maxima
    if config.MIN_DURATION < 0:
        print(f"ERRO: MIN_DURATION deve ser maior ou igual a 0, encontrado: {config.MIN_DURATION}")
        return False

    if config.MAX_DURATION < 0:
        print(f"ERRO: MAX_DURATION deve ser maior ou igual a 0, encontrado: {config.MAX_DURATION}")
        return False

    if config.MIN_DURATION >= config.MAX_DURATION:
        print(f"ERRO: MIN_DURATION ({config.MIN_DURATION}) deve ser menor que MAX_DURATION ({config.MAX_DURATION})")
        return False

    # Validar delay
    if config.DELAY_MIN < 0:
        print(f"ERRO: DELAY_MIN deve ser maior ou igual a 0, encontrado: {config.DELAY_MIN}")
        return False

    if config.DELAY_MAX < 0:
        print(f"ERRO: DELAY_MAX deve ser maior ou igual a 0, encontrado: {config.DELAY_MAX}")
        return False

    if config.DELAY_MIN >= config.DELAY_MAX:
        print(f"ERRO: DELAY_MIN ({config.DELAY_MIN}) deve ser menor que DELAY_MAX ({config.DELAY_MAX})")
        return False

    # Validar nome da pasta destino
    if len(config.NOME_PASTA_DESTINO.strip()) == 0:
        print("ERRO: NOME_PASTA_DESTINO nao pode ser vazio")
        return False

    print("Todas as configuracoes estao validas!")
    return True


if __name__ == "__main__":
    # Permite executar este arquivo diretamente para testar a validacao
    if validate_config():
        print("Config validado com sucesso!")
        sys.exit(0)
    else:
        print("Config possui erros!")
        sys.exit(1)
