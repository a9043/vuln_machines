from rest_framework import serializers
from .models import VulnerableMachine
from django.contrib.auth.models import User

class VulnerableMachineSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    
    class Meta:
        model = VulnerableMachine
        fields = [
            'id', 'name', 'vuln_id', 'type', 'status', 'wiki_link',
            'tags', 'description', 'writeups', 'os', 'has_gui', 'cases_count',
            'cases_list', 'detected_in', 'security_tools', 'esxi_version', 'os_version',
            'additional_versions', 'created_at', 'updated_at', 'creator'
        ]
    
    def validate_vuln_id(self, value):
        """Валидация vuln_id"""
        if not value:
            raise serializers.ValidationError("ID уязвимости обязателен")
        return value
    
    def validate_name(self, value):
        """Валидация name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Название машины обязательно")
        return value.strip()
    
    def validate_description(self, value):
        """Валидация description"""
        if not value or not value.strip():
            raise serializers.ValidationError("Описание обязательно")
        return value.strip()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=[('user', 'user'), ('admin', 'admin')], write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'user_type')

    def create(self, validated_data):
        user_type = validated_data.pop('user_type', 'user')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        # Устанавливаем права администратора если выбран тип admin
        if user_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user