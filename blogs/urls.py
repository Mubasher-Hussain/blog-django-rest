from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from django.shortcuts import render

 
app_name = 'blogs'

urlpatterns = [
    path('api/post_list/', views.BlogsList.as_view(), name='post_list'),
    path('api/post_list/<str:author>', views.BlogsList.as_view(), name='post_list_author'),
    path('api/post_delete/<int:pk>', views.BlogsDetail.as_view(), name='post_delete'),
    path('api/post_edit/<int:pk>', views.BlogsDetail.as_view(), name='post_edit'),
    path('api/post_detail/<int:pk>', views.BlogsDetail.as_view(), name='post_detail'),
    path('api/create_blog/', views.BlogsList.as_view(), name='post_new'),
    path('api/create_comment/<int:pk>', views.CommentsDetail.as_view(), name='comment_new'),
    path('api/comment_detail/<int:pk>', views.CommentsDetail.as_view(), name='pos_detail'),
    path('api/register/', views.register_request, name="register"),
    path('api/login/', views.login_request, name="login"),
    path('api/logout/', views.logout_request, name="logout"),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
