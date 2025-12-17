from rest_framework import viewsets
from .models import Event, Church
from .serializers import EventSerializer, ChurchSerializer
from django.utils import timezone

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('start_datetime')
    serializer_class = EventSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned events to a given date range,
        by filtering against a `start` and `end` query parameter.
        """
        queryset = super().get_queryset()
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        
        if start and end:
            # FullCalendar sends start and end dates for the view
            # We want events that overlap with this range
            queryset = queryset.filter(start_datetime__lt=end, end_datetime__gt=start)
            
        return queryset

class ChurchViewSet(viewsets.ModelViewSet):
    queryset = Church.objects.all()
    serializer_class = ChurchSerializer
