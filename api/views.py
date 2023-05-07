#Import from django
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login

#Import from rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions

#Import from api
from .serializers import UserSerializer, RegisterSerializer, BlogSerializer
from .models import Blogs
from .forms import BlogForm


#Import from knox
from knox.models import AuthToken
from knox.views import LoginView

#Register a user
class RegisterAPI(generics.GenericAPIView): #GenericAPIView is used to create a view that does not have a model instance or queryset attribute
    serializer_class = RegisterSerializer #serializer_class is the serializer that should be used for validating and deserializing input, and for serializing output

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  #get_serializer is used to get the serializer instance that should be used for validating and deserializing input, and for serializing output
        serializer.is_valid(raise_exception=True) #raise_exception=True is to raise an exception if the serializer is not valid
        user = serializer.save() #save the user
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data, #serialized representation of a user object
        "token": AuthToken.objects.create(user)[1] #create a token for the user
        })



#Login a user
class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)  #Allow any user to login(send request)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data) #data=request.data is the data that is sent in the request
        serializer.is_valid(raise_exception=True) #raise_exception=True is to raise an exception if the serializer is not valid
        user = serializer.validated_data['user'] #validated_data is the data after it has been validated
        login(request, user) #login the user
        return super(LoginAPI, self).post(request, format=None) #return the response



#Create a blog
class CreateBlog(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    serializer_class = BlogSerializer #serializer_class is the serializer that should be used for validating and deserializing input, and for serializing output

    def post(self, request, *args, **kwargs):
        user = request.user #get the user that is logged in
        form = BlogForm(request.POST, request.FILES) #create a form instance
        if form.is_valid(): #check if the form is valid
            blog = form.save(commit=False) #save the form but don't commit it to the database yet
            blog.author = user #set the author of the blog to the user that is logged in
            blog.save() #save the blog
            return Response({
                "blog": BlogSerializer(blog, context=self.get_serializer_context()).data, #serialized representation of a blog object
                "message": "Blog created successfully" #message to be returned in the response
            }, status=status.HTTP_201_CREATED) #return the response
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST) #return the errors in the form
        

from django.core.paginator import Paginator #import Paginator for Pagination


#List all blogs
class ListAllBlogs(APIView):
    permission_classes = (permissions.IsAuthenticated,)    #Allow any user to view this page
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs): #get method to get all the blogs
        blogs = Blogs.objects.all() #get all the blogs
        items_per_page = 10 # Define the number of items per page
        paginator = Paginator(blogs, items_per_page)   #Create a Paginator object
        page_number = request.GET.get('page', 1) #Get the current page number from the request query parameters
        current_page = paginator.get_page(page_number) # Get the current page from the Paginator
        serializer = BlogSerializer(current_page, many=True, context={"request": request})# Serialize the current page's data
        
        # Prepare the response data
        response_data = { 
            "Blogs": serializer.data,  #serialized representation of a blog object
            "current_page": current_page.number,  #current page number
            "total_pages": paginator.num_pages, #total number of pages
            "total_items": paginator.count, #total number of items
        }

        return Response(response_data, status=status.HTTP_200_OK) #return the response



class ListOneBlog(APIView):
    permission_classes = (permissions.IsAuthenticated,)   #Allow any user to view this page
    serializer_class = BlogSerializer

    def get(self, request, pk): 
        blogs = get_object_or_404(Blogs, id=pk) #get the blog with the id=pk
        serializer = BlogSerializer(blogs, context={"request": request}) #serialized representation of a blog object
        return Response({"Blog":serializer.data}, status=status.HTTP_200_OK) #return the response
    


class EditBlog(APIView):
    permission_classes = (permissions.IsAuthenticated,)  #Only authenticated users can view this page
    serializer_class = BlogSerializer

    def put(self, request, pk):
        user = request.user #get the user that is logged in
        blog = get_object_or_404(Blogs, id=pk) #get the blog with the id=pk
        if blog.author == user: #check if the author of the blog is the user that is logged in
            form = BlogForm(request.POST, request.FILES, instance=blog) #create a form instance
            if form.is_valid(): #check if the form is valid
                form.save() #save the form
                return Response({
                    "blog": BlogSerializer(blog, context={'request': request}).data, #serialized representation of a blog object
                    "message": "Blog updated successfully" #message to be returned in the response
                }, status=status.HTTP_200_OK) #return the response
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST) #return the errors in the form
        else:
            return Response({"message": "You are not authorized to edit this blog"}, status=status.HTTP_401_UNAUTHORIZED)
        

class DeleteBlog(APIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    serializer_class = BlogSerializer

    def delete(self, request, pk):
        user = request.user #get the user that is logged in
        blog = get_object_or_404(Blogs, id=pk) #get the blog with the id=pk
        if blog.author == user: #check if the author of the blog is the user that is logged in
            blog.delete() #delete the blog
            return Response({"message": "Blog deleted successfully"}, status=status.HTTP_200_OK) #return the response
        else:
            return Response({"message": "You are not authorized to delete this blog"}, status=status.HTTP_401_UNAUTHORIZED) #return the response