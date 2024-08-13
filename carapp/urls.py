from django.urls import path
from . import views

app_name = 'carapp'

urlpatterns = [
    path('', views.homepage, name='homepage'),  # New homepage view
    path('car-list/', views.car_list, name='car_list'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.users_profile, name='users_profile'),
]
