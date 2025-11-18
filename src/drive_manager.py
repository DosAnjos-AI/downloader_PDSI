"""
Modulo de integracao com Google Drive API usando OAuth2.
Responsavel por autenticacao, criacao de estrutura de pastas e upload de arquivos.
"""

import sys
import os
from pathlib import Path
import pickle
import logging
import time
from typing import Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


class DriveManager:
    """
    Classe responsavel por gerenciar uploads para Google Drive.

    Implementa autenticacao OAuth2, criacao de estrutura de pastas
    e upload de arquivos com sistema de retry.
    """

    # Escopo minimo: acesso apenas a arquivos criados pelo app
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    def __init__(self, credentials_path: Path, token_path: Path, destination_folder_name: str):
        """
        Inicializa o gerenciador do Google Drive.

        Args:
            credentials_path: Caminho para credentials.json (OAuth2 client)
            token_path: Caminho para salvar/carregar token.pickle
            destination_folder_name: Nome da pasta destino (ex: "audios_katube")
        """
        # Configura logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info("Inicializando DriveManager...")

        # Autentica e cria service
        self.service = self.authenticate(credentials_path, token_path)

        # Configura estrutura de pastas
        self.bd_pdsi_folder_id, self.destination_folder_id = self.setup_folder_structure(
            destination_folder_name
        )

        self.logger.info(f"DriveManager inicializado com sucesso")
        self.logger.info(f"BD_PDSI folder ID: {self.bd_pdsi_folder_id}")
        self.logger.info(f"Destination folder ID: {self.destination_folder_id}")

    def authenticate(self, credentials_path: Path, token_path: Path):
        """
        Implementa fluxo de autenticacao OAuth2 completo.

        Verifica se token salvo existe e eh valido. Se nao existe ou
        expirou, inicia fluxo OAuth2 para obter novo token.

        Args:
            credentials_path: Caminho para credentials.json
            token_path: Caminho para token.pickle

        Returns:
            service: Objeto do Google Drive API service

        Raises:
            FileNotFoundError: Se credentials.json nao existir
            Exception: Se autenticacao falhar
        """
        self.logger.info("Iniciando autenticacao OAuth2...")

        creds = None

        # Verifica se token ja existe
        if token_path.exists():
            self.logger.info(f"Token encontrado em {token_path}")
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        # Se nao ha credenciais validas, faz login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info("Token expirado, renovando...")
                try:
                    creds.refresh(Request())
                    self.logger.info("Token renovado com sucesso")
                except Exception as e:
                    self.logger.warning(f"Falha ao renovar token: {e}")
                    creds = None

            # Se ainda nao tem credenciais validas, inicia fluxo OAuth2
            if not creds:
                if not credentials_path.exists():
                    raise FileNotFoundError(
                        f"Arquivo credentials.json nao encontrado em {credentials_path}"
                    )

                self.logger.info("Iniciando fluxo OAuth2...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path),
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                self.logger.info("Autenticacao OAuth2 concluida")

            # Salva token para proxima execucao
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            self.logger.info(f"Token salvo em {token_path}")

        # Cria service do Drive API
        try:
            service = build('drive', 'v3', credentials=creds)
            self.logger.info("Google Drive API service criado com sucesso")
            return service
        except Exception as e:
            self.logger.error(f"Erro ao criar Drive API service: {e}")
            raise

    def get_or_create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        """
        Busca ou cria pasta no Google Drive.

        Busca pasta por nome. Se existe, retorna ID existente.
        Se nao existe, cria nova pasta e retorna ID.

        Args:
            folder_name: Nome da pasta
            parent_id: ID da pasta pai (None para raiz do Drive)

        Returns:
            str: ID da pasta encontrada ou criada

        Raises:
            Exception: Se operacao falhar
        """
        try:
            # Monta query de busca
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"

            # Busca pasta
            self.logger.info(f"Buscando pasta '{folder_name}'...")
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()

            files = results.get('files', [])

            if files:
                folder_id = files[0]['id']
                self.logger.info(f"Pasta '{folder_name}' encontrada: {folder_id}")
                return folder_id

            # Cria pasta se nao existe
            self.logger.info(f"Pasta '{folder_name}' nao encontrada, criando...")
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }

            if parent_id:
                file_metadata['parents'] = [parent_id]

            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()

            folder_id = folder.get('id')
            self.logger.info(f"Pasta '{folder_name}' criada: {folder_id}")
            return folder_id

        except HttpError as e:
            self.logger.error(f"Erro HTTP ao buscar/criar pasta '{folder_name}': {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro ao buscar/criar pasta '{folder_name}': {e}")
            raise

    def setup_folder_structure(self, destination_folder_name: str) -> Tuple[str, str]:
        """
        Configura estrutura de pastas no Google Drive.

        Cria ou obtem pasta BD_PDSI na raiz do Drive.
        Cria ou obtem pasta destination_folder_name dentro de BD_PDSI.

        Estrutura final: BD_PDSI/destination_folder_name/

        Args:
            destination_folder_name: Nome da pasta destino

        Returns:
            Tuple[str, str]: (bd_pdsi_folder_id, destination_folder_id)
        """
        self.logger.info("Configurando estrutura de pastas...")

        # Cria/obtem pasta BD_PDSI na raiz
        bd_pdsi_id = self.get_or_create_folder('BD_PDSI')

        # Cria/obtem pasta destino dentro de BD_PDSI
        destination_id = self.get_or_create_folder(destination_folder_name, bd_pdsi_id)

        self.logger.info("Estrutura de pastas configurada com sucesso")
        return bd_pdsi_id, destination_id

    def upload_file(self, file_path: Path, folder_id: str, retries: int = 2) -> bool:
        """
        Faz upload de arquivo para pasta especifica no Drive.

        Implementa sistema de retry para lidar com falhas temporarias.

        Args:
            file_path: Caminho local do arquivo
            folder_id: ID da pasta destino no Drive
            retries: Numero de tentativas em caso de falha

        Returns:
            bool: True se upload bem-sucedido, False caso contrario
        """
        if not file_path.exists():
            self.logger.error(f"Arquivo nao encontrado: {file_path}")
            return False

        file_name = file_path.name
        self.logger.info(f"Iniciando upload de '{file_name}' para pasta {folder_id}")

        # Tenta upload com retry
        for attempt in range(1, retries + 1):
            try:
                self.logger.info(f"Tentativa {attempt}/{retries} de upload: {file_name}")

                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }

                media = MediaFileUpload(
                    str(file_path),
                    resumable=True
                )

                uploaded_file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()

                file_id = uploaded_file.get('id')
                self.logger.info(f"Upload concluido: {file_name} (ID: {file_id})")
                return True

            except HttpError as e:
                self.logger.warning(f"Erro HTTP na tentativa {attempt}/{retries}: {e}")
                if attempt < retries:
                    time.sleep(2 ** attempt)  # Backoff exponencial: 2s, 4s
            except Exception as e:
                self.logger.warning(f"Erro na tentativa {attempt}/{retries}: {e}")
                if attempt < retries:
                    time.sleep(2 ** attempt)

        self.logger.error(f"Upload falhou apos {retries} tentativas: {file_name}")
        return False

    def upload_video_folder(self, video_id: str, temp_video_path: Path) -> bool:
        """
        Faz upload da pasta completa de um video.

        Cria pasta video_id dentro da pasta destino e faz upload
        dos arquivos .mp3 e .json.

        Args:
            video_id: ID do video do YouTube
            temp_video_path: Caminho da pasta temporaria do video

        Returns:
            bool: True se ambos uploads bem-sucedidos, False caso contrario
        """
        self.logger.info(f"Iniciando upload da pasta do video: {video_id}")

        try:
            # Cria pasta do video dentro da pasta destino
            video_folder_id = self.get_or_create_folder(video_id, self.destination_folder_id)

            # Define caminhos dos arquivos
            audio_file = temp_video_path / f"{video_id}.mp3"
            json_file = temp_video_path / f"{video_id}.json"

            # Verifica se arquivos existem
            if not audio_file.exists():
                self.logger.error(f"Arquivo de audio nao encontrado: {audio_file}")
                return False

            if not json_file.exists():
                self.logger.error(f"Arquivo JSON nao encontrado: {json_file}")
                return False

            # Upload do audio
            audio_success = self.upload_file(audio_file, video_folder_id)
            if not audio_success:
                self.logger.error(f"Falha no upload do audio: {video_id}")
                return False

            # Upload do JSON
            json_success = self.upload_file(json_file, video_folder_id)
            if not json_success:
                self.logger.error(f"Falha no upload do JSON: {video_id}")
                return False

            self.logger.info(f"Upload da pasta do video concluido: {video_id}")
            return True

        except Exception as e:
            self.logger.error(f"Erro ao fazer upload da pasta do video {video_id}: {e}")
            return False

    def upload_csv(self, csv_path: Path) -> bool:
        """
        Faz upload do arquivo CSV de metadados.

        Upload para pasta destino no Drive. Se ja existe, sobrescreve.

        Args:
            csv_path: Caminho local do arquivo CSV

        Returns:
            bool: True se upload bem-sucedido, False caso contrario
        """
        self.logger.info(f"Iniciando upload do CSV: {csv_path}")

        if not csv_path.exists():
            self.logger.error(f"Arquivo CSV nao encontrado: {csv_path}")
            return False

        # Verifica se CSV ja existe no Drive
        try:
            query = f"name='{csv_path.name}' and '{self.destination_folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()

            files = results.get('files', [])

            if files:
                # CSV ja existe, remove arquivo antigo
                old_file_id = files[0]['id']
                self.logger.info(f"CSV existente encontrado, removendo: {old_file_id}")
                self.service.files().delete(fileId=old_file_id).execute()

        except Exception as e:
            self.logger.warning(f"Erro ao verificar CSV existente: {e}")

        # Faz upload do CSV
        success = self.upload_file(csv_path, self.destination_folder_id)

        if success:
            self.logger.info("Upload do CSV concluido com sucesso")
        else:
            self.logger.error("Falha no upload do CSV")

        return success
