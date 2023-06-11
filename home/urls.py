from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('',views.home, name="home"),
    path('create-stale/', views.createStale, name="create-stale"),
    path('create-przydzielone-stale/', views.createPrzydzieloneStale, name="create-przydzielone-stale"),
    path('update-stale/<str:pk>/', views.updateStale, name="update-stale"),
    path('create-jednorazowe/', views.createJednorazowe, name="create-jednorazowe"),
    path('update-jednorazowe/<str:pk>/', views.updateJednorazowe, name="update-jednorazowe"),
]