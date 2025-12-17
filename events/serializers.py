from rest_framework import serializers
from .models import Event, Church, Speaker

class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = '__all__'

class SpeakerSerializer(serializers.ModelSerializer):
    home_church_name = serializers.ReadOnlyField(source='home_church.name')
    
    class Meta:
        model = Speaker
        fields = ['id', 'name', 'home_church', 'home_church_name']

class EventSerializer(serializers.ModelSerializer):
    host_church_name = serializers.ReadOnlyField(source='host_church.name')
    speakers = SpeakerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'
