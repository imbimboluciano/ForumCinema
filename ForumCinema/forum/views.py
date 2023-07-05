from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from polls.models import Poll

@login_required
def create_review(request):
    if request.method == "POST":
        user = request.user
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False) 
            review.user = user
            review.date_published = timezone.now()
            review.save()
            form.save()
            return redirect('home')
    
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
        context['form'] = CreateReviewForm()
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
    
    def get_redirect_field_name(self) -> str:
        return None

    

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
    
    def get_redirect_field_name(self) -> str:
        return None
    

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
    
    def get_success_url(self) -> str:
       profile = reverse("forum:profilo", kwargs={"pk": self.request.user.pk})
       return profile


class DiscoverView(LoginRequiredMixin,ListView):
    model = Review
    template_name = "forum/discover_page.html"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset()
        
        reviews_notfollowing = []
        for review in self.model.objects.all():
            if review.user.userprofile not in self.request.user.userprofile.followers.all():
                if review.user != self.request.user:
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
    template_name = "forum/result_search_page.html"

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
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = GroupsCreateForm(user = self.request.user.pk)
        return context

    


@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupsCreateForm(request.POST, user = request.user.pk)
        if form.is_valid():
            group = form.save(commit=False) 
            group.creator = request.user
            group.save()
            form.save()
            return redirect('forum:groupspage')


class GroupDetailView(LoginRequiredMixin,DetailView):
    model = CinemaClub
    template_name = "forum/group_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all().filter(group_id = self.kwargs["pk"]) 
        context["polls"] = Poll.objects.all().filter(group_id = self.kwargs["pk"]) 
        
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
    return render(request, 'forum/create_post.html', {'form': form, 'group': get_object_or_404(CinemaClub, pk=group)})


class EliminaEntitaView(LoginRequiredMixin,DeleteView):

    template_name = "forum/elimina_elemento.html"

    def get_context_data(self, **kwargs):
        context = super(EliminaEntitaView, self).get_context_data(**kwargs)
        entita = "Post"
        if self.model == Review:
            entita = "Review"
        elif self.model == Comment:
            entita = "Commento"
        elif self.model == CinemaClub:
            entita = "CinemaClub"
        
        context["entita"] = entita
        return context
    
    def get_success_url(self) -> str:
        if self.model == Review:
            return reverse("forum:profilo", args=[self.request.user.pk])
        elif self.model == Post:
            return reverse("forum:detailgroup", args=[self.kwargs["group"]])
        elif self.model == Comment:
            return reverse("forum:detailreview", args=[self.kwargs["review"]])
        elif self.model == CinemaClub:
            return reverse("forum:groupspage")
           

class EliminaReviewView(EliminaEntitaView):
    model = Review

class EliminaCommentView(EliminaEntitaView):
    model = Comment

class EliminaPostView(EliminaEntitaView):
    model = Post
    
class EliminaGroupView(EliminaEntitaView):
    model = CinemaClub


class ModificaCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "forum/modifica_commento.html"
    
    def get_success_url(self) -> str:
       profile = reverse("forum:detailreview", kwargs={"pk": self.object.review.pk})
       return profile
    
    def form_valid(self, form):
        form.instance.date_posted = timezone.now()
        return super().form_valid(form)
    

class ModificaPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = "forum/modifica_post.html"
    
    def get_success_url(self) -> str:
       profile = reverse("forum:detailgroup", kwargs={"pk": self.object.group.pk})
       return profile
    
    def form_valid(self, form):
        form.instance.date_posted = timezone.now()
        return super().form_valid(form)
    
@login_required
def search(request):
    if 'search' in request.GET:
        search_term = request.GET['search']
        if search_term:
            return HttpResponseRedirect(reverse("forum:risultatiricerca", args=[search_term]))
        
    return HttpResponseRedirect(reverse("forum:discover"))

@login_required
def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('forum:detailgroup', args=[post.group.pk]))