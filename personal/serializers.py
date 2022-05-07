
from rest_framework import serializers
from . import models


class BugReportSerializer(serializers.ModelSerializer):
    index = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    severity = serializers.CharField(required=False)
    priority = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    class Meta:
        model = models.BugReport 
        fields = ['uuid', 'owner_id', 'index', 'name', 'steps', 'fact_result', 
        'exp_result', 'desc', 'priority', 'severity', 'status', 'url', 'created_at']

    def update(self, instance, validated_data):
        if validated_data.get('status') is not None:
            instance.status = validated_data.get('status')
        if validated_data.get('url') is not None:
            instance.url = validated_data.get('url')
        if validated_data.get('severity') is not None:
            instance.severity = validated_data.get('severity')
        if validated_data.get('priority') is not None:
            instance.priority = validated_data.get('priority')
        if validated_data.get('desc') is not None:
            instance.desc = validated_data.get('desc')
        if validated_data.get('exp_result') is not None:
            instance.exp_result = validated_data.get('exp_result')
        if validated_data.get('fact_result') is not None:
            instance.fact_result = validated_data.get('fact_result')
        if validated_data.get('steps') is not None:
            instance.steps = validated_data.get('steps')
        if validated_data.get('name') is not None:
            instance.name = validated_data.get('name')
        if validated_data.get('index') is not None:
            instance.index = validated_data.get('index')

        instance.save()
        return instance

    def create(self, validated_data):
        return models.BugReport.objects.create(**validated_data, owner=self.context['request'].user)


class BugReportListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BugReport
        fields = ['uuid', 'owner_id', 'index', 'name', 'status', 'severity', 'priority']
