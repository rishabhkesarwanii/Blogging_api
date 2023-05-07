from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        

from django.core.paginator import Paginator

class ListAllBlogs(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        blogs = Blogs.objects.all()
        items_per_page = 10 # Define the number of items per page
        paginator = Paginator(blogs, items_per_page)   #Create a Paginator object
        page_number = request.GET.get('page', 1) #Get the current page number from the request query parameters
        current_page = paginator.get_page(page_number) # Get the current page from the Paginator
        serializer = BlogSerializer(current_page, many=True, context={"request": request})# Serialize the current page's data
        
        # Prepare the response data
        response_data = {
            "Blogs": serializer.data,
            "current_page": current_page.number,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
        }

        return Response(response_data, status=status.HTTP_200_OK)



class ListOneBlog(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BlogSerializer

    def get(self, request, pk):
        blogs = get_object_or_404(Blogs, id=pk)
        serializer = BlogSerializer(blogs, context={"request": request})
        return Response({"Blog":serializer.data}, status=status.HTTP_200_OK)
    


class EditBlog(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogSerializer

    def put(self, request, pk):
        user = request.user
        blog = get_object_or_404(Blogs, id=pk)
        if blog.author == user:
            form = BlogForm(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                form.save()
                return Response({
                    "blog": BlogSerializer(blog, context={'request': request}).data,
                    "message": "Blog updated successfully"
                }, status=status.HTTP_200_OK)
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You are not authorized to edit this blog"}, status=status.HTTP_401_UNAUTHORIZED)
        

class DeleteBlog(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogSerializer

    def delete(self, request, pk):
        user = request.user
        blog = get_object_or_404(Blogs, id=pk)
        if blog.author == user:
            blog.delete()
            return Response({"message": "Blog deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not authorized to delete this blog"}, status=status.HTTP_401_UNAUTHORIZED)