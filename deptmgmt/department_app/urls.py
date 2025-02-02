# department_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # here listed all the urls that can be accessed by the user
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('add-department/', views.add_department, name='add_department'),
    path('edit-department/<int:pk>/', views.edit_department, name='edit_department'),
    path('delete-department/<int:pk>/', views.delete_department, name='delete_department'),
]


