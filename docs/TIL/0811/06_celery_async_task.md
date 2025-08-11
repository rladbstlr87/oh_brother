# Celery Task 실제 구현 코드
## 1. `@shared_task`를 이용한 작업 정의

### ex.1-1: 문서 처리 작업 (`process_document`)
```py
from .processor import FileProcessor

@shared_task
def process_document(document_id):
    processor = FileProcessor(document_id)
    processor.process()
    return f"Document {document_id} processed."
```
- `FileProcessor`의 무거운 파일 처리 로직을 비동기적으로 실행하기 위해 `process_document` 태스크로 정의
- `document_id`를 인자로 받아 백그라운드에서 파일 파싱, OCR, 이미지 변환 등을 수행

## 2. `.delay()`를 이용한 작업 호출 및 연동

### ex.2-1: 스크레이핑과 파일 처리 연동 (`collect_band_documents`)
```py
@shared_task
def collect_band_documents():
    scraper = BandScraper()
    # ... 스크레이핑 및 SourceDocument 저장 로직 ...
    
    for post in posts_data:
        # ...
        doc = SourceDocument(...)
        doc.save()
        
        # 새로 생성된 문서 객체의 ID를 인자로 전달하여 처리 작업을 호출
        process_document.delay(doc.id)
    
    # ...
    return f"{new_docs_count} new documents collected."
```
- `collect_band_documents` 작업 내에서 다른 작업인 `process_document`를 `.delay()`로 호출
- 데이터 수집 후, 실제 파일 처리는 별도의 워커에게 위임하는 파이프라인을 구성하여 두 작업을 분리
