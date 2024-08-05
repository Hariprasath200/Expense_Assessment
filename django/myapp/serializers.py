# myapp/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'role')
from rest_framework import serializers
from .models import Expense
from rest_framework import serializers
from .models import Expense

from rest_framework import serializers
from .models import Expense

from rest_framework import serializers
from .models import Expense

from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    created_by_email = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'name', 'date_of_expense', 'category', 'description', 'amount', 'created_by', 'created_by_email', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_created_by_email(self, obj):
        return obj.created_by.email if obj.created_by else None

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)

# serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role']  # Include any other fields you need

