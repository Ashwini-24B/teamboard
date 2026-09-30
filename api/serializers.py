from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, KBEntry, QueryLog


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'role', 'created_at']


class KBEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = KBEntry
        fields = ['id', 'question', 'answer', 'category', 'created_at']


class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = ['id', 'company', 'search_term', 'results_count', 'queried_at']
        read_only_fields = ['company', 'queried_at']


class RegistrationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'company_name']

    def create(self, validated_data):
        company_name = validated_data.pop('company_name')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        user.company.company_name = company_name
        user.company.save(update_fields=['company_name'])

        return user