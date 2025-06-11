# poll/urls.py (or whatever your main project folder is named)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('mypollapp.urls')),
    # Include the URLs from the mypollapp app
    path('admin/', admin.site.urls),
    # Django admin interface
]
