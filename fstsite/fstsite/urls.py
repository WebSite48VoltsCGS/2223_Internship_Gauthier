"""
URL configuration for fstsite project.

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
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import API.view as apiv

router = routers.SimpleRouter()

router.register('article', apiv.ArticleViewset, basename='article')
router.register('admin/article', apiv.AdminArticleViewSet, basename='admin-article')
router.register('component', apiv.ComponentViewset, basename='component')
router.register('admin/component', apiv.AdminComponentViewSet, basename='admin-component')
router.register('client', apiv.ClientViewset, basename='client')
router.register('admin/client', apiv.AdminClientViewSet, basename='admin-client')
router.register('command', apiv.CommandViewset, basename='command')
router.register('admin/command', apiv.AdminCommandViewSet, basename='admin-command')
router.register('command-line', apiv.CommandLineViewset, basename='command-line')
router.register('admin/command-line', apiv.AdminCommandLineViewSet, basename='admin-command-line')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("devis/", include("sql_test.urls")),
]
