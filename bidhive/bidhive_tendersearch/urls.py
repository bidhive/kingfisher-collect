"""bidhive_tendersearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework_nested import routers

from bidhive_tendersearch.tender.views import TenderViewSet, RecentTenderViewSet

router = routers.SimpleRouter()
router.register("tender", TenderViewSet, basename="tender")
router.register("recent-tender", RecentTenderViewSet, basename="recent-tender")

urlpatterns = [path("admin/", admin.site.urls), path("", include(router.urls))]
