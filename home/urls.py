from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('',views.home, name="home"),
    path('create-stale/', views.createStale, name="create-stale"),
    path('create-przydzielone-stale/', views.createPrzydzieloneStale, name="create-przydzielone-stale"),
    path('start-stale/<str:pk>/', views.startStale, name="start-stale"),
    path('finish-stale/<str:pk>/', views.finishStale, name="finish-stale"),
    path('edit-stale/<str:pk>/', views.editStale, name="edit-stale"),
    path('create-jednorazowe/', views.createJednorazowe, name="create-jednorazowe"),
    path('start-jednorazowe/<str:pk>/', views.startJednorazowe, name="start-jednorazowe"),
    path('finish-jednorazowe/<str:pk>/', views.finishJednorazowe, name="finish-jednorazowe"),
    path('edit-jednorazowe/<str:pk>/', views.editJednorazowe, name="edit-jednorazowe"),
    path('generate-raport-jednorazowy/', views.generateJednorazowy, name="generate-raport-jednorazowy"),
    path('generate-raport-staly/', views.generateStaly, name="generate-raport-staly"),
    path('generate-edited-dates-report/', views.createEditedDatesReport, name="create-edited-dates-raport"),
    path('generate-all-tasks-report/', views.generateAllTasksReport, name="generate-all-tasks-report"),
    path('generate-specific-tasks-report/', views.generateSpecificTasks, name="generate-specific-tasks-report"),
    path('generate-user-tasks-report/<int:user_id>/', views.showGeneratedUserTasksReport, name='generate-user-tasks-report'),
    path('generate-user-tasks-report-csv/<int:user_id>/', views.exportUserTasksReportCSV, name='generate-user-tasks-report-csv'),
    path('generate-user-tasks-report-pdf/<int:user_id>/', views.exportUserTasksReportPDF, name='generate-user-tasks-report-pdf'),
    path('generate-user-tasks-report-html/<int:user_id>/', views.exportUserTasksReportHTML, name='generate-user-tasks-report-html'),
]