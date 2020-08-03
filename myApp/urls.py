from django.urls import path
from . import views

urlpatterns = [
    path('helloworld/', views.helloworld, name='helloworld'),
    path('', views.post_list, name='post_list'),
    path('create_post/', views.create_post, name='create_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('activate/<str:encoded>/<str:token>/', views.activate, name="activate"),
    path('sign_up_confirm/<str:email>/', views.sign_up_confirm, name='sign_up_confirm'),
    path('my_page/', views.my_page, name='my_page'),
]

