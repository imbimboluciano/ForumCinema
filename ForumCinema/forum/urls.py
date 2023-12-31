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
from django.urls import path, re_path
from .views import *

app_name = "forum"

urlpatterns = [
    path('pubblicarecensione/',create_review, name = "pubblicareview"),
    path('profilo/<pk>', ProfiloDetailView.as_view(), name="profilo"),
    path('modificaprofilo/', update_profile,name = "modificaprofilo"),
    path('aggiungifilm/', FavoritiesMovieUpdate.as_view(), name="aggiungifilm"),
    path('reviewlike/<int:pk>/', ReviewLike, name = "reviewlike"),
    path('postlike/<int:pk>/', PostLike, name = "postlike"),
    path('dettaglireview/<int:pk>/', ReviewDetailView.as_view(), name = "detailreview"),
    path('dettaglireview/<int:id>/commenta', add_comment_review, name = "commentareview"),
    path("followuser/<int:author>/",followToggle, name="followuser"),
    path("modificareview/<int:pk>/", ReviewUpdateView.as_view(), name = "modificareview"),
    path("discover/", DiscoverView.as_view(), name = "discover"),
    path("followerlist/<pk>/", FollowListView.as_view(), name = "followlist" ),
    path("allfavoritiesmovie/<pk>", AllFavoritiesMovieList.as_view(), name = "allfavoritiesmovie" ),
    path("groupspage/", GroupsListView.as_view(), name = "groupspage"),
    path("creagroup/", create_group, name = "creategroup"),
    path("groupdetail/<pk>/",GroupDetailView.as_view(), name = "detailgroup"),
    path("createpost/<int:group>/", create_post_group, name = "createpost"),
    path("cancellareview/<pk>", EliminaReviewView.as_view(), name = "cancellareview"),
    path("cancellacommento/<pk>/<int:review>", EliminaCommentView.as_view(), name = "cancellacommento"),
    path("cancellapost/<pk>/<int:group>", EliminaPostView.as_view(), name = "cancellapost"),
    path("eliminagruppo/<pk>/", EliminaGroupView.as_view(), name = "eliminagruppo"),
    path('modificacommento/<pk>/', ModificaCommentView.as_view(), name = "updatecomment"),
    path('modificapost/<pk>/', ModificaPostView.as_view(), name = "updatepost"),
    path('ricerca/', search, name = "ricerca"),
    path('risultatiricerca/<str:ricerca>/', SearchDiscoverListView.as_view(), name = "risultatiricerca")



]

