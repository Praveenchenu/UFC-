from .models import Fighter_Details
from rest_framework import serializers

class FightersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter_Details
        fields = ['id', 'Name', 'Weight_class', 'Age', 'Prof_record', 'p4p_rank']

