from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User
from games.models import Game

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_id', 'game', 'wins', 'losses', 'time_created']
        read_only_fields = ['user_id', 'game', 'wins', 'losses', 'time_created']
        
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
        
    def validate(self, attrs):
        temporary = attrs.get('temporary', False)
        if temporary:
            if not attrs.get('username'):
                attrs['username'] = generateName()

        if not temporary:
            errors = {}
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if not attrs.get(field) and not getattr(self.instance, field, None):
                    errors[field] = f'Field is required for non-temporary users.'
            if errors:
                raise ValidationError(errors)
        if attrs.get('email'):
            attrs['email'] = self.__class__.Meta.model.objects.normalize_email(attrs.get('email'))
        return attrs
