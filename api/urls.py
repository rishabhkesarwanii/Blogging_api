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
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', knox_views.LogoutView.as_view()),

    #Blogs
    path('create', CreateBlog.as_view()),
    path('posts/', ListAllBlogs.as_view()),
    path('posts/<int:pk>', ListOneBlog.as_view()),
    path('posts/<int:pk>/edit', EditBlog.as_view()),
    path('posts/<int:pk>/delete', DeleteBlog.as_view()),
    
]