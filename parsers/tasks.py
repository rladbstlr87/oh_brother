from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .scraper import BandScraper
from .processor import FileProcessor
from events.models import SourceDocument

@shared_task
def process_document(document_id):
    processor = FileProcessor(document_id)
    processor.process()
    return f"Document {document_id} processed."

@shared_task
def collect_band_documents():
    scraper = BandScraper()
    try:
        scraper.login()
        posts = scraper.get_posts()
        
        for post in posts:
            # This is a simplified example. 
            # We need to implement logic to check for attachments vs. text
            # and to avoid duplicates.
            post_text = post.get_text()
            
            # Create a SourceDocument for each post
            # This is a placeholder - proper logic is needed
            if not SourceDocument.objects.filter(extracted_text=post_text).exists():
                # In a real scenario, you would download the file and save it here
                # For now, we just save the text
                doc = SourceDocument.objects.create(extracted_text=post_text, status='수집완료')
                # After creating the document, trigger the processing task
                process_document.delay(doc.id)

    finally:
        scraper.close()
    
    return f"{len(posts)} posts processed."
