from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('',views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('stale/<str:pk>/', views.stale, name="stale"),
    path('create-stale/', views.createStale, name="create-stale"),
    path('update-stale/<str:pk>/', views.updateStale, name="update-stale"),
    path('jednorazowe/<str:pk>/', views.jednorazowe, name="jednorazowe"),
    path('create-jednorazowe/', views.createJednorazowe, name="create-jednorazowe"),
    path('update-jednorazowe/<str:pk>/', views.updateJednorazowe, name="update-jednorazowe"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
]