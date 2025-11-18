"""
Script principal do downloader_PDSI.
Orquestra todo o fluxo: validacao, download, metadados e upload para Google Drive.
"""

import sys
import shutil
from pathlib import Path

import config
from src.config_validator import validate_config
from src.youtube_downloader import YouTubeDownloader
from src.metadata_manager import MetadataManager
from src.drive_manager import DriveManager
from src.utils import (
    setup_logging,
    load_downloaded_ids,
    add_downloaded_id,
    is_downloaded,
    sanitize_filename
)


def main():
    """
    Funcao principal que executa o fluxo completo de processamento.
    """

    # ==========================================================================
    # 1. INICIALIZACAO
    # ==========================================================================

    print("\n" + "="*70)
    print("DOWNLOADER_PDSI - Download de audios do YouTube para Google Drive")
    print("="*70 + "\n")

    # Valida configuracao
    print("[INFO] Validando configuracoes...")
    if not validate_config():
        print("[ERRO] Configuracao invalida. Corrija os erros e execute novamente.")
        sys.exit(1)
    print("[INFO] Configuracao valida\n")

    # Cria estrutura de pastas
    temp_dir = Path("temp")
    logs_dir = Path("logs")
    input_dir = Path("input")

    temp_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)
    input_dir.mkdir(exist_ok=True)

    # Configura logging
    processing_logger, error_logger = setup_logging(logs_dir)
    processing_logger.info("="*70)
    processing_logger.info("Iniciando processamento")
    processing_logger.info("="*70)

    # Carrega log de IDs ja processados
    log_path = logs_dir / "downloaded_ids.json"
    downloaded_ids = load_downloaded_ids(log_path)
    processing_logger.info(f"IDs ja processados: {len(downloaded_ids)}")

    # ==========================================================================
    # 2. AUTENTICACAO GOOGLE DRIVE
    # ==========================================================================

    print("[INFO] Autenticando Google Drive...")
    processing_logger.info("Iniciando autenticacao Google Drive")

    credentials_path = Path("credentials.json")
    token_path = Path("token.pickle")

    # Verifica se credentials.json existe
    if not credentials_path.exists():
        msg = (
            "Arquivo credentials.json nao encontrado!\n"
            "\n"
            "Para usar este projeto, voce precisa:\n"
            "1. Criar um projeto no Google Cloud Console\n"
            "2. Ativar a Google Drive API\n"
            "3. Criar credenciais OAuth 2.0\n"
            "4. Baixar o arquivo credentials.json\n"
            "5. Colocar credentials.json na raiz do projeto\n"
            "\n"
            "Consulte a documentacao para mais detalhes."
        )
        print(f"\n[ERRO] {msg}\n")
        error_logger.error("credentials.json nao encontrado")
        sys.exit(1)

    try:
        drive_manager = DriveManager(
            credentials_path,
            token_path,
            config.NOME_PASTA_DESTINO
        )
        print("[INFO] Autenticacao bem-sucedida\n")
        processing_logger.info("Autenticacao Google Drive concluida")
    except Exception as e:
        print(f"\n[ERRO] Falha na autenticacao: {e}\n")
        error_logger.error(f"Falha na autenticacao Google Drive: {e}")
        sys.exit(1)

    # ==========================================================================
    # 3. COLETA DE LINKS
    # ==========================================================================

    urls_to_process = []

    if config.USE_BATCH_FILE:
        print("[INFO] Modo: BATCH_FILE")
        processing_logger.info("Modo: BATCH_FILE")

        # Busca primeiro arquivo .txt em input/
        txt_files = list(input_dir.glob("*.txt"))

        if not txt_files:
            msg = "Nenhum arquivo .txt encontrado na pasta input/"
            print(f"\n[ERRO] {msg}\n")
            error_logger.error(msg)
            sys.exit(1)

        batch_file = txt_files[0]
        print(f"[INFO] Arquivo encontrado: {batch_file}")
        processing_logger.info(f"Arquivo batch: {batch_file}")

        # Le arquivo linha por linha
        with open(batch_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Remove linhas vazias e espacos
        urls_to_process = [line.strip() for line in lines if line.strip()]

        print(f"[INFO] URLs encontradas: {len(urls_to_process)}\n")
        processing_logger.info(f"Total de URLs no batch: {len(urls_to_process)}")

    else:
        print("[INFO] Modo: URL_UNICA")
        processing_logger.info("Modo: URL_UNICA")
        urls_to_process = [config.URL]
        print(f"[INFO] URL: {config.URL}\n")
        processing_logger.info(f"URL a processar: {config.URL}")

    # ==========================================================================
    # 4. PROCESSAMENTO DE CADA URL
    # ==========================================================================

    # Contadores totais
    total_success = 0
    total_failures = 0
    total_skipped = 0

    for url_index, url in enumerate(urls_to_process, 1):
        print("-" * 70)
        print(f"[INFO] Processando URL {url_index}/{len(urls_to_process)}: {url}")
        print("-" * 70)
        processing_logger.info(f"Processando URL {url_index}/{len(urls_to_process)}: {url}")

        try:
            # Instancia YouTubeDownloader
            yt_downloader = YouTubeDownloader(temp_dir)

            # Detecta tipo da URL
            url_type = yt_downloader.detect_url_type(url)

            # Extrai lista de video IDs
            video_ids = yt_downloader.extract_video_ids(url)

            print(f"[INFO] Tipo detectado: {url_type} ({len(video_ids)} videos)")
            processing_logger.info(f"Tipo: {url_type}, Total de videos: {len(video_ids)}")

            # Contadores da URL atual
            url_success = 0
            url_failures = 0
            url_skipped = 0

            # Instancia MetadataManager para esta URL
            csv_output = temp_dir / "metadata.csv"
            metadata_manager = MetadataManager(temp_dir, csv_output)

            # Processa cada video
            for video_index, video_id in enumerate(video_ids, 1):

                # Verifica se ja foi processado
                if is_downloaded(video_id, downloaded_ids):
                    print(f"[SKIP] [{video_index}/{len(video_ids)}] Video {video_id} ja processado")
                    processing_logger.info(f"[{video_index}/{len(video_ids)}] Skip: {video_id}")
                    url_skipped += 1
                    continue

                print(f"[INFO] [{video_index}/{len(video_ids)}] Baixando: {video_id}")
                processing_logger.info(f"[{video_index}/{len(video_ids)}] Iniciando: {video_id}")

                try:
                    # Extrai metadados
                    metadata = yt_downloader.extract_metadata(video_id)

                    # Valida metadados
                    if not metadata_manager.validate_metadata_integrity(metadata):
                        raise Exception("Metadados invalidos")

                    # Salva JSON individual
                    metadata_manager.save_json_metadata(video_id, metadata)

                    # Adiciona ao batch para CSV
                    metadata_manager.add_metadata_to_batch(metadata)

                    # Baixa audio
                    download_success = yt_downloader.download_audio(video_id)

                    if not download_success:
                        raise Exception("Falha no download do audio")

                    # Faz upload para Drive
                    video_path = temp_dir / video_id
                    upload_success = drive_manager.upload_video_folder(video_id, video_path)

                    if not upload_success:
                        raise Exception("Falha no upload para Drive")

                    # Upload bem-sucedido: adiciona em downloaded_ids
                    add_downloaded_id(video_id, log_path)
                    downloaded_ids.add(video_id)

                    # Deleta pasta temporaria
                    if video_path.exists():
                        shutil.rmtree(video_path)

                    print(f"[INFO] Upload concluido: {video_id}")
                    processing_logger.info(f"[{video_index}/{len(video_ids)}] Sucesso: {video_id}")
                    url_success += 1

                    # Aplica delay randomico (exceto no ultimo video)
                    if video_index < len(video_ids):
                        yt_downloader.apply_random_delay()

                except Exception as e:
                    print(f"[ERRO] Falha no video {video_id}: {e}")
                    error_logger.error(f"Falha no video {video_id}: {e}")
                    url_failures += 1

            # Consolida CSV com metadados desta URL
            if metadata_manager.metadata_list:
                print(f"[INFO] Consolidando metadados em CSV...")
                processing_logger.info("Consolidando metadata.csv")

                if metadata_manager.consolidate_csv():
                    # Upload do CSV para Drive
                    if csv_output.exists():
                        drive_manager.upload_csv(csv_output)
                        csv_output.unlink()  # Remove CSV local apos upload

                # Limpa batch
                metadata_manager.clear_batch()

            # Estatisticas da URL
            print(f"\n[INFO] Estatisticas URL {url_index}:")
            print(f"        Sucesso: {url_success}")
            print(f"        Falhas: {url_failures}")
            print(f"        Skip: {url_skipped}\n")

            processing_logger.info(
                f"Estatisticas URL {url_index}: "
                f"{url_success} sucesso, {url_failures} falhas, {url_skipped} skip"
            )

            # Atualiza contadores totais
            total_success += url_success
            total_failures += url_failures
            total_skipped += url_skipped

        except Exception as e:
            print(f"[ERRO] Erro ao processar URL: {e}")
            error_logger.error(f"Erro ao processar URL {url}: {e}")
            continue

    # ==========================================================================
    # 5. FINALIZACAO
    # ==========================================================================

    print("\n" + "="*70)
    print("[INFO] PROCESSAMENTO CONCLUIDO")
    print("="*70)
    print(f"[INFO] Estatisticas Totais:")
    print(f"        Total Sucesso: {total_success}")
    print(f"        Total Falhas: {total_failures}")
    print(f"        Total Skip: {total_skipped}")
    print(f"        Total Processado: {total_success + total_skipped}")
    print("="*70 + "\n")

    processing_logger.info("="*70)
    processing_logger.info(
        f"Processamento concluido: "
        f"{total_success} sucesso, {total_failures} falhas, {total_skipped} skip"
    )
    processing_logger.info("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Processamento interrompido pelo usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERRO FATAL] {e}\n")
        sys.exit(1)
