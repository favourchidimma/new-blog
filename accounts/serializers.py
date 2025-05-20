from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password





User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        
class OtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)       
        

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(max_length = 200)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    
    old_password = serializers.CharField(max_length=100, write_only=True)
    new_password = serializers.CharField(max_length=100, write_only=True)
    
    def validate_old_password(self, value):
        
        user = self.context['request'].user
        
        if user.check_password(value):
            
            return value
        else:
            raise serializers.ValidationError('Password does not match our record')
        
        
    def validate_new_password(self, value):

        validate_password(value)
        return value

        
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
