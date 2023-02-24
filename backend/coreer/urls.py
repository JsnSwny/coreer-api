from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('accounts.urls')),
    path('', include("chat.urls")),
    path('', include("recsys.urls")),
    path('admin/', admin.site.urls),
]