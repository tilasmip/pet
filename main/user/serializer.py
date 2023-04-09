from rest_framework import serializers
from main.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'gender', 'address',
                  'mobile', 'profile_image', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Confirmation password got wrong.")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ['password', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'address',
                  'mobile', 'gender', 'profile_image']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=50, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=50, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password2')
        if p1 != p2:
            raise serializers.ValidationError(
                'Confirmation password didn\'t match.')
        self.set_password(p1)
        return attrs

    def set_password(self, password):
        user = self.context.get('user')
        user.set_password(password)
        user.save()


class RequestPasswordResetSerializer(serializers.Serializer):
    user = {}
    email = serializers.EmailField(max_length=200)
    mobile = serializers.CharField(max_length=20)

    class Meta:
        fields = ['email', 'mobile']

    def validate(self, attrs):
        email = attrs.get('email')
        mobile = attrs.get('mobile')
        if User.objects.filter(email=email, mobile=mobile).exists():
            self.user = User.objects.get(email=email)
            return attrs
        raise serializers.ValidationError({'msg': 'Invalid data.'})

    def get_user_id(self):
        email = self.data.get('email')
        uid = urlsafe_base64_encode(force_bytes(self.user.id))
        return uid

    def get_token_for_password_reset(self):
        token = PasswordResetTokenGenerator().make_token(self.user)
        return token


class UserPasswordResetSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        max_length=50, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=50, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password1', 'password2']

    def validate(self, attrs):
        try:
            password1 = attrs.get('password1')
            password2 = attrs.get('password2')
            if password1 != password2:
                return serializers.ValidationError({'msg': 'Comfirmation password didn\' match.'})
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            print(id, token)
            user = User.objects.get(pk=id)
            if user is None:
                raise serializers.ValidationError(
                    {'msg': 'Invalid token or uid.'})
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({'msg': 'Invalid token.'})
            user.set_password(password1)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as tokenerror:
            raise serializers.ValidationError({'msg': 'Invalid token.'})


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'mobile', 'profile_image', 'address', 'gender']

    def validate(self, attrs):
        return attrs
