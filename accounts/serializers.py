from rest_framework import serializers
from accounts.models import Account,FriendRequest, Friends
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password Dosn't Match"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})
        
        account = User(username=username, first_name=first_name, last_name=last_name, email=email)
        account.set_password(password)
        account.is_active = False
        account.save()

        Account.objects.create(
            user = account,
        )
        # print(account)
        return account
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Account
        # exclude = ['user']
        fields = ['id','user','image_url', 'phone_no', 'city', 'description' ]
        read_only_fields = ['user',]
        # fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class FriendRequestSerializer(serializers.ModelSerializer):#
    class Meta:
        model = FriendRequest
        fields = ['id','sender', 'receiver']
        read_only_fields = ['sender']


class FriendSerializer(serializers.ModelSerializer):#

    class Meta:
        model = Friends
        fields = ['id', 'receiver_account', 'sender_account']