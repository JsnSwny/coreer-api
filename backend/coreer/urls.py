from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('accounts.urls')),
    path("chat/", include("chat.urls")),
    path('admin/', admin.site.urls),
]