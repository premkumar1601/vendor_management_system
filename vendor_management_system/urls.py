"""vendor_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from venders_and_orders.urls import urlpatterns as venders_and_orders_urls 
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='admin:index', permanent=False)),
    path('api/token/', obtain_auth_token, name='token'),
    path('admin/', admin.site.urls),
    path('', include(venders_and_orders_urls)),
]
