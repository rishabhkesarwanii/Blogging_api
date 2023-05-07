from rest_framework import serializers #import serializers from rest_framework
from django.contrib.auth.models import User #import the User model
from .models import Blogs #import the Blogs model


# User Serializer
class UserSerializer(serializers.ModelSerializer): #ModelSerializer for the User model
    class Meta:
        model = User 
        fields = ('id', 'username', 'email') #fields that will be returned in the response



# Register Serializer
class RegisterSerializer(serializers.ModelSerializer): #ModelSerializer for the User model
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}   #This is to make sure that the password is not returned in the response

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password']) #create a new user

        return user #return the user


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ('id','title', 'content', 'image')
        read_only_fields = ('id',) #fields that will be returned in the response and cannot be edited