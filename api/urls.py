from django.urls import path, include
from knox import views as knox_views

from .views import (
    RegisterAPI, 
    LoginAPI,
    CreateBlog,
    ListAllBlogs,
    ListOneBlog,
    EditBlog,
    DeleteBlog,
)

urlpatterns = [
    
    #Authentication
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view()),

    #Blogs
    path('create', CreateBlog.as_view(), name='create-blog'),
    path('posts/', ListAllBlogs.as_view(), name='list-all-blogs'),
    path('posts/<int:pk>', ListOneBlog.as_view(), name='list-one-blog'),
    path('posts/<int:pk>/edit', EditBlog.as_view(), name='edit-blog'),
    path('posts/<int:pk>/delete', DeleteBlog.as_view(), name='delete-blog'),
    
]