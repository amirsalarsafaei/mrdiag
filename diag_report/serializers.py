from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import DiagReport, BatteryHealth, SubmitTicket, File


class DiagReportSerializer(serializers.ModelSerializer):
    ticket = serializers.UUIDField(write_only=True, required=True)
    camera_test_id = serializers.UUIDField(write_only=True)
    mic_test_id = serializers.UUIDField(write_only=True)
    camera_test_file_url = serializers.SerializerMethodField()
    mic_test_file_url = serializers.SerializerMethodField()

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
            'ticket',
            'device_hardware',
            'camera_test_id', 'mic_test_id', 'camera_test_file_url', 'mic_test_file_url'
        ]

        read_only_fields = ('image',)

    def get_camera_test_file_url(self, obj):
        request = self.context.get('request')
        if obj.camera_test.file and hasattr(obj.camera_test.file, 'url'):
            return request.build_absolute_uri(obj.camera_test.file.url)
        return None

    def get_mic_test_file_url(self, obj):
        request = self.context.get('request')
        if obj.mic_test.file and hasattr(obj.mic_test.file, 'url'):
            return request.build_absolute_uri(obj.mic_test.file.url)
        return None

    def to_representation(self, instance):
        data = super(DiagReportSerializer, self).to_representation(instance)
        battery_health_enum = BatteryHealth(int(data['battery_health']))
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

    def create(self, validated_data):
        camera_test_id = validated_data.pop('camera_test_id')
        mic_test_id = validated_data.pop('mic_test_id')
        camera_test = File.objects.get(file_id=camera_test_id)
        mic_test = File.objects.get(file_id=mic_test_id)

        diag_report = DiagReport.objects.create(camera_test=camera_test, mic_test=mic_test, **validated_data)
        return diag_report

    def update(self, instance, validated_data):
        instance.camera_test = File.objects.get(
            file_id=validated_data.get('camera_test_id', instance.camera_test.file_id))
        instance.mic_test = File.objects.get(file_id=validated_data.get('mic_test_id', instance.mic_test.file_id))
        instance.save()
        return instance


class SubmitDiagReportSerializer(serializers.Serializer):
    ticket = serializers.UUIDField()


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_id', 'file']
        read_only_fields = ('file_id', )
