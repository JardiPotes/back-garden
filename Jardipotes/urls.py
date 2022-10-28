from django.contrib import admin
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('api/users/', include('accounts.urls')),

]
