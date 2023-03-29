from django.contrib import admin
from django.urls import path, include  # include added

urlpatterns = [
    path('login/', include('users.urls')),  # include the URLs of the users app
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),

]
