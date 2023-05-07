from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login

#Import from rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions


from .serializers import UserSerializer, RegisterSerializer, BlogSerializer
from .models import Blogs
from .forms import BlogForm


#Import from knox
from knox.models import AuthToken
from knox.views import LoginView

#Register a user
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data, #serialized representation of a user object
        "token": AuthToken.objects.create(user)[1]
        })

#Login a user
class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)  #Allow any user to login(send request)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data) #data=request.data is the data that is sent in the request
        serializer.is_valid(raise_exception=True) #raise_exception=True is to raise an exception if the serializer is not valid
        user = serializer.validated_data['user'] #validated_data is the data after it has been validated
        login(request, user) #login the user
        return super(LoginAPI, self).post(request, format=None)


class CreateBlog(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    serializer_class = BlogSerializer

    def post(self, request, *args, **kwargs):
        user = request.user #get the user that is logged in
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = user
            blog.save()
            return Response({
                "blog": BlogSerializer(blog, context=self.get_serializer_context()).data,
                "message": "Blog created successfully"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ListAllBlogs(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        blogs = Blogs.objects.all()
        serializer = BlogSerializer(blogs, many=True, context={"request": request})
        return Response({"Blogs":serializer.data}, status=status.HTTP_200_OK)
    


class ListOneBlog(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BlogSerializer

    def get(self, request, pk):
        blogs = get_object_or_404(Blogs, id=pk)
        serializer = BlogSerializer(blogs, context={"request": request})
        return Response({"Blog":serializer.data}, status=status.HTTP_200_OK)