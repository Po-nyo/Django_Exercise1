from django.urls import path
from . import views

urlpatterns = [
    path('helloworld/', views.helloworld, name='helloworld'),
    path('', views.post_list, name='post_list'),
    path('create_post/', views.create_post, name='create_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('my_page/', views.my_page, name='my_page'),
    path('author/<str:username>/', views.post_list_by_author, name='post_list_by_author'),
    path('visualization_service/', views.visualization_service, name='visualization_service'),
    path('visualization_view/', views.visualization_view, name='visualization_view'),
]

