from __future__ import absolute_import, unicode_literals
import os
import requests
import tempfile
from celery import shared_task
from django.core.files import File

from .scraper import BandScraper
from .processor import FileProcessor
from events.models import SourceDocument

@shared_task
def process_document(document_id):
    # 기존 로직과 동일
    processor = FileProcessor(document_id)
    processor.process()
    return f"Document {document_id} processed."

@shared_task
def collect_band_documents():
    scraper = BandScraper()
    new_docs_count = 0
    try:
        scraper.login()
        # 스크레이퍼는 {'text': str, 'attachment_urls': list, 'timestamp': str} 형태의 딕셔너리 리스트를 반환
        posts_data = scraper.get_posts_with_details()

        with tempfile.TemporaryDirectory() as temp_dir:
            for post in posts_data:
                post_text = post.get('text', '').strip()
                attachment_urls = post.get('attachment_urls', [])
                timestamp = post.get('timestamp')

                # --- CASE 1: 첨부파일(이미지)가 있는 경우 ---
                if attachment_urls:
                    for attachment_url in attachment_urls:
                        # 고유 식별자 = "타임스탬프_이미지URL"
                        unique_id = f"{timestamp}_{attachment_url}"
                        if SourceDocument.objects.filter(unique_identifier=unique_id).exists():
                            continue
                        
                        try:
                            response = requests.get(attachment_url, stream=True)
                            response.raise_for_status()
                            
                            file_name = os.path.basename(attachment_url).split('?')[0]
                            temp_file_path = os.path.join(temp_dir, file_name)
                            
                            with open(temp_file_path, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            # 각 이미지마다 SourceDocument 생성
                            doc = SourceDocument(
                                unique_identifier=unique_id,
                                extracted_text=post_text # 게시글 본문은 모든 관련 문서에 저장
                            )
                            with open(temp_file_path, 'rb') as f:
                                doc.original_file.save(file_name, File(f), save=True)
                            
                            doc.status = '수집완료'
                            doc.save()
                            process_document.delay(doc.id)
                            new_docs_count += 1

                        except requests.exceptions.RequestException as e:
                            print(f"다운로드 실패 {attachment_url}: {e}")
                            continue
                
                # --- CASE 2: 텍스트만 있는 경우 ---
                elif post_text and timestamp:
                    if SourceDocument.objects.filter(unique_identifier=timestamp).exists():
                        continue
                    
                    doc = SourceDocument(
                        unique_identifier=timestamp,
                        extracted_text=post_text,
                        status='처리완료' # 파일 후처리 불필요
                    )
                    doc.save()
                    new_docs_count += 1

    finally:
        scraper.close()
    
    return f"{new_docs_count} new documents collected."