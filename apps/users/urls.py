"""syslong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import LoginView
from .views import MenuView
from .views import UsersView
from .views import PermsView
from .views import RoleView
from .views import PermsListView

router = DefaultRouter()
router.register('users', UsersView, basename='users_oper')
router.register('roles', RoleView, basename='roles_oper')
urlpatterns = [
    url(r'^login$', LoginView.as_view()),
    url(r'^menu$', MenuView.as_view()),
    url(r'^perms/$', PermsView.as_view()),
    url(r'^permslist/$', PermsListView.as_view()),
    # url(r'^users', UsersView.as_view({'get': 'list'})),
    url('', include(router.urls))
]
