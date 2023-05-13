from rest_framework import serializers
from .models import Table

class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ('pk', 'name', 'capacity', 'log_is_active', 'log_date_created', 'log_date_last_update')