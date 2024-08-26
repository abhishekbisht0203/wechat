from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('friendlist/', views.friendlist, name='friendlist'),
    path('send_message/<int:id>', views.send_message, name='send_message'),
    path('chat/<int:id>/', views.chat, name='chat'),
]