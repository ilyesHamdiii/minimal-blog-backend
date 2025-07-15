from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_view),
    path('',views.signup),
    path('home/',views.home),
    path('mypost/',views.mypost),
    path('newpost/',views.newpost),
    path('signout/',views.signout),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]

