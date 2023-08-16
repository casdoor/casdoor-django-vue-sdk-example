"""
URL configuration for casdoor_django_js_sdk_example project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signin', SignIn.as_view(), name='signin'),
    path('toLogin', ToLogin.as_view(), name='tologin'),
    path('api/signout', SignOut.as_view(), name='signout'),
    path('api/get-account', Account.as_view(), name='get-account'),
]
