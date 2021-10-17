from django.urls import path
from my_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<int:id>', views.editevent, name='editevent'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('register/', views.register, name='register'),
]