"""toolcase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
# Use include() to add paths from the catalog application
from django.conf.urls import include
from django.views.generic import RedirectView
# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    *i18n_patterns(path('admin/', admin.site.urls)),
    # path('rosetta/', include('rosetta.urls')),
    *i18n_patterns(path('toolfamily/', include('toolfamily.urls'))),
    *i18n_patterns(path('accounts/login/', RedirectView.as_view(url='/toolfamily/', permanent=True))),
    *i18n_patterns(path('', RedirectView.as_view(url='/toolfamily/home/', permanent=True))),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
# urlpatterns += i18n_patterns(
#     path('toolfamily/', include('toolfamily.urls'))+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
