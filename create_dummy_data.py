import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from events.models import Event, Church

def create_data():
    church, created = Church.objects.get_or_create(
        name="테스트 교회",
        defaults={'address': '서울시 강남구', 'website': 'http://example.com'}
    )
    
    Event.objects.create(
        title="2025 신년 부흥성회",
        start_datetime=timezone.now() + timedelta(days=1),
        end_datetime=timezone.now() + timedelta(days=4),
        location="대성전",
        host_church=church,
        description="이것은 테스트 집회입니다."
    )
    
    print("Dummy data created!")

if __name__ == '__main__':
    create_data()
