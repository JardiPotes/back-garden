from django.contrib import admin
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static


""" 
POST ${API_URL}/ - request a reset password token by using the email parameter
POST ${API_URL}/confirm/ - using a valid token, the users password is set to the provided password
POST ${API_URL}/validate_token/ - will return a 200 if a given token is valid
"""

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('api/users/', include('accounts.urls')),



]
