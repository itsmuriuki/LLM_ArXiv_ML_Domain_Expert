import re 
import subprocess
from datetime import datetime
from io import BytesIO
from typing import Dict, Tuple 
from xml.etree import ElementTree as ET

import requests 
from docling.datamodel.base_models import DocumentStream, InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions, TesseractOcrOptions
from docling.document_converter import ConversionError, DocumentConverter, PdfFormatOption
from loguru import logger 

from llm_arxiv.domain.documents import ExpertDocument, PaperDocument 

class ArxivClient:
    """"
    Singleton client for managing arxiv API connections and OCR processing,
    Handles paper metadata fetching, PDF doenloading and OCT processing  
    """

    _instance  = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # initialize all lonlived objects here 
            cls._instance._session = requests.Session()
            cls._instance._ocr = OCRClient() #Single OCR client instance 
        return cls._instance
    
    def _fetch_metadata(self, arxiv_url: str) -> Tuple[bool, Dict]:
        # Extract arxiv id from URL 
        arxiv_id =  arxiv_url.split('/')[1]

        # Fetch metadata
        metadata_url =  f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        metadata_response = self._session.get(metadata_url)  

        if metadata_response.status_code != 200:
            logger.error(f"Failed to fetch metadata for {arxiv_url}: {metadata_response.status_code}")
            return False, ()
        
        logger.info(f"Fetched metadata for {arxiv_url} successfully")

        # Parse metadata
        metadata_root = ET.fromstring(metadata_response.content)
        namespace = 





