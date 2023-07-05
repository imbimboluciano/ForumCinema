"""
URL configuration for ForumCinema project.

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
from django.urls import path, re_path, include
from .views import *
from forum.views import *
from django.contrib.auth import views as auth_views
from .initcmds import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$|^/$|^home/$',ReviewListView.as_view(),name = "home"),
    path("register/", signup, name="register"),
    re_path(r"activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",activate, name='activate'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
	path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name = "change_password.html", success_url = '/'),name='change_password'),
    path('forum/', include("forum.urls")),
    path('polls/', include("polls.urls"))


]

#init_avatar_table()

#erase_movie_table()
#provafilm()
#initMovieDB()
#citazione_table()
