import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files import File
from events.models import SourceDocument
from parsers.tasks import process_document

def run():
    print("Starting the test process...")
    file_path = './media/source_documents/인천 부평중부 - 복음 유튜브 채널 안내.pdf'
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # Create a SourceDocument instance
    doc = SourceDocument()
    with open(file_path, 'rb') as f:
        doc.original_file.save('인천 부평중부 - 복음 유튜브 채널 안내.pdf', File(f), save=True)
    
    print(f"SourceDocument with ID {doc.id} created.")

    # Trigger the Celery task
    print("Dispatching process_document task...")
    process_document.delay(doc.id)
    print("Task dispatched successfully.")

if __name__ == '__main__':
    run()
