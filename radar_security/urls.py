from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

import dashboard
from users import views

LOGIN_URL = '/login'

urlpatterns = [
    path('', views.user_login, name='login'),  # Set the empty path as the login page
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('logout/', dashboard.views.logout_view, name='logout'),
    path('test_404/', TemplateView.as_view(template_name='404.html')),

]
