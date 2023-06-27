from typing import Any, Dict
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
            context['randomuser'] = User.objects.all()
            print(context['randomuser'])
            return context

        randomuser = []
        for user in User.objects.all():
            if user.userprofile not in self.request.user.userprofile.followers.all():
                randomuser.append(user.pk)
        context['randomuser'] = User.objects.filter(pk__in=randomuser)
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
    return render(request, 'forum/commenta_review.html', {'form': form})
    
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
    