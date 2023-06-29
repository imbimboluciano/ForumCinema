from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, get_list_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .models import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone


class CreateReviewView(LoginRequiredMixin,CreateView):
    model = Review
    template_name = "forum/create_review.html"
    success_url = reverse_lazy("home")
    fields = ["movie", "descrizione"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReviewListView(ListView):
    model = Review
    template_name = "home.html"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset()
        
        reviews_following = []
        for review in self.model.objects.all():
            if review.user.userprofile in self.request.user.userprofile.followers.all():
                reviews_following.append(review)

        return reviews_following
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['randomuser'] = User.objects.all().exclude(is_staff=True)
            return context

        randomuser = []

        for user in User.objects.all():
            if user.userprofile in self.request.user.userprofile.followers.all():
                randomuser.append(user.pk)
        context['randomuser'] = User.objects.all().exclude(pk__in=randomuser).exclude(pk=self.request.user.pk).exclude(is_staff=True)
        return context

class ReviewDetailView(LoginRequiredMixin,DetailView):
    model = Review
    template_name = "forum/review_detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Review, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data
    

class ProfiloDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = "forum/profilo.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['myreview'] = Review.objects.filter(user=self.kwargs['pk'])
        userprofile = get_object_or_404(UserProfile, user=self.kwargs['pk'])
        context["firstfourfavoritiesmovie"] = userprofile.favorities.all()[:4]
        print(context['firstfourfavoritiesmovie'])
        return context

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('forum:profilo', pk=request.user.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'forum/modifica_profilo.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

class FavoritiesMovieUpdate(CreateView):
    model = UserProfile
    fields = "__all__"
    template_name = "forum/favorities_movie.html"

@login_required
def ReviewLike(request, pk):
    post = get_object_or_404(Review, id=request.POST.get('review_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('forum:detailreview', args=[str(pk)]))

@login_required
def add_comment_review(request, id):
    if request.method == "POST":
        user = request.user
        review = get_object_or_404(Review, pk=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save( commit=False)  # returns new unsaved comment object
            comment.user = user
            comment.review = review
            comment.date_posted = timezone.now()
            comment.save()
            return redirect('forum:detailreview', review.id)
    else:
        form = CommentForm()
        review = get_object_or_404(Review, pk=id)
    return render(request, 'forum/commenta_review.html', {'form': form, 'review':review})
    
@login_required
def followToggle(request, author):
    authorObj = UserProfile.objects.get(user_id=author)
    currentUserObj = UserProfile.objects.get(user_id=request.user)
    following = authorObj.following.all()

    if author != currentUserObj.user:
        if currentUserObj in following:
            authorObj.following.remove(currentUserObj.id)
        else:
            authorObj.following.add(currentUserObj.id)

    return HttpResponseRedirect(reverse("forum:profilo", args=[authorObj.user.pk]))
    

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewUpdateForm
    template_name = "forum/modifica_review.html"
    success_url = reverse_lazy("home")


class DiscoverView(LoginRequiredMixin,ListView):
    model = Review
    template_name = "forum/discover_page.html"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset()
        
        reviews_notfollowing = []
        for review in self.model.objects.all():
            if review.user.userprofile not in self.request.user.userprofile.followers.all():
                reviews_notfollowing.append(review)

        return reviews_notfollowing
    
class FollowListView(LoginRequiredMixin,DetailView):
    model = User
    template_name = "forum/followers_list.html"


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User,pk = self.kwargs["pk"])
        context["followers"] = user.userprofile.following.all()
        print(context["followers"])
        context["following"] = user.userprofile.followers.all()
        print(context["following"])

        return context
    
class AllFavoritiesMovieList(LoginRequiredMixin,DetailView):
    model = User
    template_name = "forum/all_favorities_movie.html"


class SearchDiscoverListView(LoginRequiredMixin,ListView):
    model = Review
    template_name = "forum/search_result.html"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset()
        
        reviews_notfollowing = []
        for review in self.model.objects.all():
            if self.kwargs["ricerca"] in review.movie.titolo:   
                if review.user.userprofile not in self.request.user.userprofile.followers.all():
                    reviews_notfollowing.append(review)

        return reviews_notfollowing
    

class GroupsListView(LoginRequiredMixin, ListView):
    model = CinemaClub
    template_name = "forum/groups_page.html"

    def get_queryset(self) -> QuerySet[Any]:
        my_club = []
        for cinemaclub in self.model.objects.all():  
            if cinemaclub.creator == self.request.user or self.request.user in cinemaclub.members.all():
                my_club.append(cinemaclub)
        
        return my_club



@login_required
def create_group(request):
    if request.method == "POST":
        user = request.user
        form = GroupsCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.creator = user
            comment.save()
            form.save()
            return redirect('forum:groupspage')
    else:
        form = GroupsCreateForm()
    return render(request, 'forum/create_group.html', {'form': form})


class GroupDetailView(LoginRequiredMixin,DetailView):
    model = CinemaClub
    template_name = "forum/group_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all().filter(group_id = self.kwargs["pk"]) 
        return context
    


@login_required
def create_post_group(request, group):
    if request.method == "POST":
        user = request.user
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) 
            post.creator = user
            post.group = get_object_or_404(CinemaClub, pk = group)
            post.date_posted = timezone.now()
            post.save()
            form.save()
            return HttpResponseRedirect(reverse("forum:detailgroup", args=[group]))
    else:
        form = PostCreateForm()
    return render(request, 'forum/create_post.html', {'form': form})