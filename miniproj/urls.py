"""miniproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, reverse_lazy
from castlefinder.views import index
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from castlefinder.views import index, show

def root_redirect(request):
    return redirect(reverse_lazy('index'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('castlefinder/', index, name= "index"),
    path('castles/<int:castle_id>', show, name='show'),
    path('', root_redirect)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
