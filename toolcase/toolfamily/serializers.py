from toolfamily.models import Case, Report
from rest_framework import serializers

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'
        # fields = ['case_id', 'publisher', 'title', 'description', 'reward', 'location','started_datetime','ended_datetime','num','constraint', 'case_status', 'pageviews','work']
        # read_only_fields = ['case_status', 'pageviews','publisher']
        # read_only_fields = ['case_status']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['reporter', 'reported_case', 'reported_user', 'report_type', 'description', 'is_treated', 'is_valid']