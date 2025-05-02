"""
URL configuration for Softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from os.path import basename

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewSet
from desk.views import ProjectViewSet, IssueViewSet, CommentViewSet


# Router for authentication app, taking care of user model
user_router = routers.SimpleRouter()
user_router.register('users', UserViewSet, basename='user')

# Router for desk app, managing the objects
desk_router = routers.DefaultRouter()
desk_router.register(r'projects', ProjectViewSet, basename='project')
desk_router.register(r'issues', IssueViewSet, basename='issue')
desk_router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(user_router.urls)),
    path('api/', include(desk_router.urls)),
]
