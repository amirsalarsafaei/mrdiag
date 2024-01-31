from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import DiagReport, BatteryHealth, SubmitTicket


class DiagReportSerializer(serializers.ModelSerializer):
    ticket = serializers.UUIDField(write_only=True)

    class Meta:
        model = DiagReport
        fields = [
            'battery_health',
            'available_memory',
            'total_memory',
            'device_model',
            'device_brand',
            'device_board',
            'device_manufacturer',
            'device_product',
            'os_version',
            'image',
            'ticket'
        ]

        read_only_fields = ('image',)

    def to_representation(self, instance):
        data = super(DiagReportSerializer, self).to_representation(instance)
        battery_health_enum = BatteryHealth[data['battery_health']]
        data['battery_health'] = battery_health_enum.name
        return data

    def to_internal_value(self, data):
        if 'battery_health' in data:
            try:
                data['battery_health'] = BatteryHealth[data['battery_health'].upper()].value
            except KeyError:
                raise serializers.ValidationError({'battery_health': 'Invalid battery health status'})
        return super(DiagReportSerializer, self).to_internal_value(data)

    @staticmethod
    def validate_ticket(value):
        try:
            value = SubmitTicket.objects.get(ticket=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("This ticket is not valid.")

        return value


class SubmitDiagReportSerializer(serializers.Serializer):
    ticket = serializers.UUIDField()
