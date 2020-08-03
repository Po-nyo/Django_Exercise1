from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('activate/<str:encoded>/<str:token>/', views.activate, name="activate"),
    path('sign_up_confirm/<str:email>/', views.sign_up_confirm, name='sign_up_confirm'),
]