from django.urls import path, include
from knox import views as knox_views

from .views import (
    RegisterAPI, 
    LoginAPI,
    CreateBlog,
    ListAllBlogs,
    ListOneBlog,
)

urlpatterns = [
    
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),

    path('create/', CreateBlog.as_view()),
    path('listall/', ListAllBlogs.as_view()),
    path('list/<int:pk>/', ListOneBlog.as_view()),
]