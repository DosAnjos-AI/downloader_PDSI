"""
Modulo de gerenciamento de metadados CSV e JSON.
Responsavel por salvar metadados individuais e consolidar em CSV.
"""

import sys
import os
from pathlib import Path
import json
import csv
import logging
from typing import Optional

# Adiciona o diretorio raiz ao path para importar modulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import sanitize_metadata_field


class MetadataManager:
    """
    Classe responsavel por gerenciar metadados de videos.

    Salva metadados individuais em JSON e consolida todos em um CSV
    com formato pipe-separated.
    """

    def __init__(self, temp_dir: Path, csv_output_path: Path):
        """
        Inicializa o gerenciador de metadados.

        Args:
            temp_dir: Diretorio temporario onde ficam os arquivos JSON
            csv_output_path: Caminho completo do arquivo CSV de saida
        """
        self.temp_dir = temp_dir
        self.output_csv_path = csv_output_path
        self.metadata_list: list[dict] = []

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

        self.logger.info(f"MetadataManager inicializado: temp_dir={temp_dir}, csv={csv_output_path}")

    def save_json_metadata(self, video_id: str, metadata: dict) -> bool:
        """
        Salva metadados completos em formato JSON.

        Cria arquivo temp/video_id/video_id.json com todos os metadados
        do video em formato JSON legivel.

        Args:
            video_id: ID do video do YouTube
            metadata: Dicionario com metadados completos

        Returns:
            bool: True se salvou com sucesso, False caso contrario
        """
        try:
            # Define caminho do arquivo JSON
            video_dir = self.temp_dir / video_id
            json_path = video_dir / f"{video_id}.json"

            # Garante que o diretorio existe
            video_dir.mkdir(parents=True, exist_ok=True)

            # Salva JSON com formatacao legivel
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Metadados JSON salvos: {json_path}")
            return True

        except Exception as e:
            self.logger.error(f"Erro ao salvar JSON para {video_id}: {str(e)}")
            return False

    def add_metadata_to_batch(self, metadata: dict) -> None:
        """
        Adiciona metadados a lista de batch para consolidacao.

        Os metadados serao incluidos no CSV quando consolidate_csv()
        for chamado.

        Args:
            metadata: Dicionario com metadados do video
        """
        self.metadata_list.append(metadata)
        self.logger.info(f"Metadados adicionados ao batch: {metadata.get('id', 'unknown')} (total: {len(self.metadata_list)})")

    def consolidate_csv(self) -> bool:
        """
        Consolida todos os metadados em arquivo CSV.

        Cria arquivo CSV pipe-separated com todos os metadados
        acumulados em metadata_list. Aplica sanitizacao em todos
        os campos de texto.

        Formato: id|title|duration|upload_date|uploader|uploader_id|view_count|like_count|comment_count

        Returns:
            bool: True se consolidou com sucesso, False caso contrario
        """
        if not self.metadata_list:
            self.logger.warning("Nenhum metadado para consolidar")
            return False

        try:
            # Define campos do CSV na ordem correta
            fieldnames = [
                'id',
                'title',
                'duration',
                'upload_date',
                'uploader',
                'uploader_id',
                'view_count',
                'like_count',
                'comment_count'
            ]

            # Garante que o diretorio de saida existe
            self.output_csv_path.parent.mkdir(parents=True, exist_ok=True)

            # Escreve CSV com separador pipe
            with open(self.output_csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                    delimiter='|',
                    extrasaction='ignore'
                )

                # Escreve header
                writer.writeheader()

                # Processa e escreve cada linha
                for metadata in self.metadata_list:
                    # Cria linha sanitizada
                    row = {}

                    # Campos de texto - sanitiza
                    row['id'] = sanitize_metadata_field(str(metadata.get('id', 'Unknown')))
                    row['title'] = sanitize_metadata_field(str(metadata.get('title', 'Unknown')))
                    row['upload_date'] = sanitize_metadata_field(str(metadata.get('upload_date', 'Unknown')))
                    row['uploader'] = sanitize_metadata_field(str(metadata.get('uploader', 'Unknown')))
                    row['uploader_id'] = sanitize_metadata_field(str(metadata.get('uploader_id', 'Unknown')))

                    # Campos numericos - garante valor inteiro
                    row['duration'] = metadata.get('duration', 0) if metadata.get('duration') is not None else 0
                    row['view_count'] = metadata.get('view_count', 0) if metadata.get('view_count') is not None else 0
                    row['like_count'] = metadata.get('like_count', 0) if metadata.get('like_count') is not None else 0
                    row['comment_count'] = metadata.get('comment_count', 0) if metadata.get('comment_count') is not None else 0

                    writer.writerow(row)

            self.logger.info(f"CSV consolidado com sucesso: {self.output_csv_path} ({len(self.metadata_list)} registros)")
            return True

        except Exception as e:
            self.logger.error(f"Erro ao consolidar CSV: {str(e)}")
            return False

    def clear_batch(self) -> None:
        """
        Limpa a lista de metadados do batch.

        Deve ser chamado apos consolidar o CSV com sucesso
        para liberar memoria.
        """
        count = len(self.metadata_list)
        self.metadata_list.clear()
        self.logger.info(f"Batch limpo: {count} registros removidos")

    def validate_metadata_integrity(self, metadata: dict) -> bool:
        """
        Valida integridade dos metadados.

        Verifica se todos os campos obrigatorios estao presentes
        e se os tipos de dados estao corretos.

        Args:
            metadata: Dicionario com metadados a validar

        Returns:
            bool: True se metadados sao validos, False caso contrario
        """
        # Campos obrigatorios
        required_fields = [
            'id',
            'title',
            'duration',
            'upload_date',
            'uploader',
            'uploader_id',
            'view_count',
            'like_count',
            'comment_count'
        ]

        # Verifica presenca de todos os campos
        for field in required_fields:
            if field not in metadata:
                self.logger.error(f"Campo obrigatorio ausente: {field}")
                return False

        # Valida tipos de campos numericos
        numeric_fields = ['duration', 'view_count', 'like_count', 'comment_count']
        for field in numeric_fields:
            value = metadata.get(field)
            if value is not None and not isinstance(value, int):
                self.logger.error(f"Campo {field} deve ser int, encontrado: {type(value).__name__}")
                return False

        # Valida tipos de campos de texto
        text_fields = ['id', 'title', 'upload_date', 'uploader', 'uploader_id']
        for field in text_fields:
            value = metadata.get(field)
            if value is not None and not isinstance(value, str):
                self.logger.error(f"Campo {field} deve ser str, encontrado: {type(value).__name__}")
                return False

        self.logger.info(f"Metadados validados com sucesso: {metadata.get('id', 'unknown')}")
        return True
