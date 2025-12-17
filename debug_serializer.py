import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from events.models import Event
from events.serializers import EventSerializer

try:
    event = Event.objects.first()
    print(f"Event: {event}")
    serializer = EventSerializer(event)
    print(serializer.data)
except Exception as e:
    import traceback
    traceback.print_exc()
