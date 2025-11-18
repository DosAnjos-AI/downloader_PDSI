"""
Modulo core de download de audios do YouTube usando yt-dlp.
Responsavel por detectar tipo de URL, extrair IDs, metadados e baixar audios.
"""

import sys
import os
from pathlib import Path
import subprocess
import json
import time
import logging
from typing import Optional

# Adiciona o diretorio raiz ao path para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.utils import random_delay


class YouTubeDownloader:
    """
    Classe responsavel por gerenciar downloads de audio do YouTube.

    Utiliza yt-dlp para extrair metadados e baixar audios de videos,
    playlists e canais do YouTube.
    """

    def __init__(self, temp_dir: Path):
        """
        Inicializa o downloader do YouTube.

        Args:
            temp_dir: Diretorio temporario para downloads
        """
        self.temp_dir = temp_dir
        self.config = config

        # Configura logger basico
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Adiciona handler se nao existir
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info(f"YouTubeDownloader inicializado com temp_dir: {temp_dir}")

    def detect_url_type(self, url: str) -> str:
        """
        Detecta o tipo de URL do YouTube.

        Analisa a estrutura da URL para determinar se e um video,
        playlist ou canal.

        Args:
            url: URL do YouTube

        Returns:
            str: Tipo da URL - "video", "playlist" ou "channel"

        Exemplo:
            >>> detector.detect_url_type("https://youtube.com/watch?v=abc")
            "video"
            >>> detector.detect_url_type("https://youtube.com/playlist?list=PLxxx")
            "playlist"
            >>> detector.detect_url_type("https://youtube.com/@channel/videos")
            "channel"
        """
        url_lower = url.lower()

        # Detecta playlist
        if "playlist?" in url_lower or "&list=" in url_lower:
            self.logger.info(f"URL detectada como playlist: {url}")
            return "playlist"

        # Detecta canal (formato @channel ou /c/ ou /channel/)
        if ("/@" in url_lower or "/c/" in url_lower or
            "/channel/" in url_lower or "/user/" in url_lower):
            self.logger.info(f"URL detectada como channel: {url}")
            return "channel"

        # Por padrao, considera video unico
        self.logger.info(f"URL detectada como video: {url}")
        return "video"

    def extract_video_ids(self, url: str) -> list[str]:
        """
        Extrai IDs de videos de uma URL do YouTube.

        Usa yt-dlp com --flat-playlist para extrair IDs sem baixar.
        Funciona para videos unicos, playlists e canais.

        Args:
            url: URL do YouTube

        Returns:
            list[str]: Lista de IDs de videos

        Raises:
            RuntimeError: Se ocorrer erro ao extrair IDs
        """
        self.logger.info(f"Extraindo IDs de videos da URL: {url}")

        try:
            # Comando yt-dlp para extrair IDs
            cmd = [
                "yt-dlp",
                "--flat-playlist",
                "--get-id",
                url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Processa output (um ID por linha)
            video_ids = [line.strip() for line in result.stdout.split('\n') if line.strip()]

            self.logger.info(f"Extraidos {len(video_ids)} video(s): {video_ids}")
            return video_ids

        except subprocess.CalledProcessError as e:
            error_msg = f"Erro ao extrair IDs da URL {url}: {e.stderr}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado ao extrair IDs: {str(e)}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

    def extract_metadata(self, video_id: str) -> dict:
        """
        Extrai metadados completos de um video do YouTube.

        Usa yt-dlp com --dump-json para obter todas as informacoes
        do video sem baixa-lo.

        Args:
            video_id: ID do video do YouTube

        Returns:
            dict: Dicionario com metadados do video contendo:
                - id: ID do video
                - title: Titulo do video
                - duration: Duracao em segundos
                - upload_date: Data de upload (YYYYMMDD)
                - uploader: Nome do canal
                - uploader_id: ID do canal
                - view_count: Numero de visualizacoes
                - like_count: Numero de likes
                - comment_count: Numero de comentarios

        Raises:
            RuntimeError: Se ocorrer erro ao extrair metadados
        """
        self.logger.info(f"Extraindo metadados do video: {video_id}")

        try:
            # Comando yt-dlp para extrair metadados
            cmd = [
                "yt-dlp",
                "--dump-json",
                "--no-playlist",
                f"https://www.youtube.com/watch?v={video_id}"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Parse JSON
            metadata_raw = json.loads(result.stdout)

            # Extrai campos relevantes e trata valores None
            metadata = {
                'id': metadata_raw.get('id', video_id),
                'title': metadata_raw.get('title', 'Unknown'),
                'duration': metadata_raw.get('duration', 0),
                'upload_date': metadata_raw.get('upload_date', 'Unknown'),
                'uploader': metadata_raw.get('uploader', 'Unknown'),
                'uploader_id': metadata_raw.get('uploader_id', 'Unknown'),
                'view_count': metadata_raw.get('view_count', 0) or 0,
                'like_count': metadata_raw.get('like_count', 0) or 0,
                'comment_count': metadata_raw.get('comment_count', 0) or 0
            }

            self.logger.info(f"Metadados extraidos: {metadata['title']} ({metadata['duration']}s)")
            return metadata

        except subprocess.CalledProcessError as e:
            error_msg = f"Erro ao extrair metadados do video {video_id}: {e.stderr}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        except json.JSONDecodeError as e:
            error_msg = f"Erro ao decodificar JSON dos metadados: {str(e)}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado ao extrair metadados: {str(e)}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

    def download_audio(self, video_id: str) -> bool:
        """
        Baixa o audio de um video do YouTube.

        Cria pasta temporaria, baixa o audio usando yt-dlp com as
        configuracoes definidas em config.py. Aplica filtros de duracao.
        Sistema de retry: 1 tentativa adicional em caso de falha.

        Args:
            video_id: ID do video do YouTube

        Returns:
            bool: True se download foi bem-sucedido, False caso contrario
        """
        self.logger.info(f"Iniciando download do audio: {video_id}")

        # Cria pasta temp/video_id/
        video_dir = self.temp_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)

        # Monta comando yt-dlp
        output_template = str(video_dir / f"{video_id}.%(ext)s")

        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", self.config.AUDIO_FORMAT,
            "--audio-quality", str(self.config.AUDIO_QUALITY),
            "--match-filter",
            f"duration >= {self.config.MIN_DURATION} & duration <= {self.config.MAX_DURATION}",
            "-o", output_template,
            "--no-playlist",
            f"https://www.youtube.com/watch?v={video_id}"
        ]

        # Tenta baixar com retry
        max_retries = 2
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.info(f"Tentativa {attempt}/{max_retries} de download: {video_id}")

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )

                self.logger.info(f"Download concluido com sucesso: {video_id}")
                return True

            except subprocess.CalledProcessError as e:
                self.logger.warning(f"Falha na tentativa {attempt}/{max_retries}: {e.stderr}")

                # Se foi a ultima tentativa, retorna False
                if attempt == max_retries:
                    self.logger.error(f"Download falhou apos {max_retries} tentativas: {video_id}")
                    return False

                # Aguarda antes de tentar novamente
                time.sleep(2)

        return False

    def apply_random_delay(self) -> None:
        """
        Aplica um delay randomico entre downloads.

        Usa a funcao random_delay do modulo utils com os valores
        configurados em DELAY_MIN e DELAY_MAX para evitar bloqueios
        por requisicoes muito frequentes.
        """
        delay = random_delay(self.config.DELAY_MIN, self.config.DELAY_MAX)
        self.logger.info(f"Aplicando delay de {delay} segundos...")
        time.sleep(delay)
        self.logger.info("Delay concluido")
