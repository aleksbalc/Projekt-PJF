from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('',views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-stale/', views.createStale, name="create-stale"),
    path('update-stale/<str:pk>/', views.updateStale, name="update-stale"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
]