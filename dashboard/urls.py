from django.urls import path

from . import views
from .views import alert_view, ip_malicious_view

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),
    path('fetch_app_data/', views.fetch_app_data, name='fetch_app_data'),
    path('fetch_typing_data/', views.fetch_typing_data, name='fetch_typing_data'),
    path('fetch_ram_data/', views.fetch_ram_data, name='fetch_ram_data'),
    path('fetch_cpu_data/', views.fetch_cpu_data, name='fetch_cpu_data'),
    path('logout/', views.logout_view, name='logout'),
    path('fetch_nids_data/', views.fetch_nids_data, name='fetch_nids_data'),
    path('alerts/', alert_view, name='alerts'),
    path('notifications/', ip_malicious_view, name='ip_malicious_view'),

]
