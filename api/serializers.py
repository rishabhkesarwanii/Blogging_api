from rest_framework import serializers #import serializers from rest_framework
from django.contrib.auth.models import User #import the User model
from .models import Blogs #import the Blogs model


# User Serializer
class UserSerializer(serializers.ModelSerializer): #ModelSerializer for the User model
    class Meta:
        model = User 
        fields = ('id', 'username', 'email') #fields that will be returned in the response


class ChangePasswordSerializer(serializers.Serializer): #Serializer for changing the password
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer): #ModelSerializer for the User model
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password') #fields that will be returned in the response
        extra_kwargs = {'password': {'write_only': True}}   #This is to make sure that the password is not returned in the response

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password']) #create a new user

        return user #return the user


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ('id','title', 'content', 'image', 'date_created', 'author') #fields that will be returned in the response
        read_only_fields = ('id','date_created', 'author',) #fields that will be returned in the response and cannot be edited