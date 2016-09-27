from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Report
        read_only_fields = ('user',)