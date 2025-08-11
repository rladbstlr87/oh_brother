import os
import tempfile
from pathlib import Path
from django.core.files.base import ContentFile
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pdfplumber

from events.models import SourceDocument

class FileProcessor:
    def __init__(self, document_id):
        self.document = SourceDocument.objects.get(id=document_id)
        self.file_path = self.document.original_file.path
        self.file_extension = Path(self.file_path).suffix.lower()

    def process(self):
        if self.file_extension == '.pdf':
            self._process_pdf()
        elif self.file_extension in ['.jpg', '.jpeg', '.png']:
            self._process_image()
        
        self.document.status = '처리완료'
        self.document.save()

    def _process_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Try to extract text directly from the first page
            try:
                with pdfplumber.open(self.file_path) as pdf:
                    first_page = pdf.pages[0]
                    text = first_page.extract_text()
                    if text and len(text.strip()) > 20:
                        self.document.extracted_text = text
                    else:
                        self.document.extracted_text = self._ocr_first_page_of_pdf(temp_dir)
            except Exception:
                self.document.extracted_text = self._ocr_first_page_of_pdf(temp_dir)

            # 2. Convert subsequent pages to WebP
            images = convert_from_path(self.file_path, first_page=2, output_folder=temp_dir)
            if images:
                self._save_image_as_webp(images[0])

    def _ocr_first_page_of_pdf(self, temp_dir):
        images = convert_from_path(self.file_path, first_page=1, last_page=1, output_folder=temp_dir)
        if images:
            return pytesseract.image_to_string(images[0], lang='kor+eng')
        return ""

    def _process_image(self):
        img = Image.open(self.file_path)
        self.document.extracted_text = pytesseract.image_to_string(img, lang='kor+eng')
        self._save_image_as_webp(img)

    def _save_image_as_webp(self, image_obj):
        webp_path = Path(self.file_path).with_suffix('.webp')
        buffer = ContentFile(b'')
        # Ensure image is in RGB mode for saving as WEBP
        if image_obj.mode != 'RGB':
            image_obj = image_obj.convert('RGB')
        image_obj.save(fp=buffer, format='WEBP')
        self.document.webp_file.save(webp_path.name, buffer, save=True)
