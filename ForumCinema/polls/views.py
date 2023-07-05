from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import Poll, Choice, Vote
from .forms import PollAddForm, EditPollForm, ChoiceAddForm
from django.http import HttpResponse
from forum.models import CinemaClub
from django.urls import reverse_lazy, reverse



@login_required()
def polls_add(request, group):
    if request.method == 'POST':
        form = PollAddForm(request.POST)
        if form.is_valid:
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.group = get_object_or_404(CinemaClub, pk = group)
            poll.save()
            form.save()
            new_choice1 = Choice(poll=poll, choice_text=form.cleaned_data['choice1']).save()
            new_choice2 = Choice(poll=poll, choice_text=form.cleaned_data['choice2']).save()
            return HttpResponseRedirect(reverse('forum:detailgroup', args=[group]))
    else:
        form = PollAddForm()
        context = {'form': form, 'group': group}
        return render(request, 'polls/add_poll.html', context)
   


@login_required
def polls_edit(request, pk, group):
    poll = get_object_or_404(Poll, pk=pk)
    if request.user != poll.owner:
        return HttpResponseRedirect(reverse('forum:detailgroup', args=[group]))

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('forum:detailgroup', args=[group]))
    else:
        form = EditPollForm(instance=poll)
        choice_form = ChoiceAddForm()

    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll, "group": group, 'choice_form': choice_form})


@login_required
def polls_delete(request, pk, group):
    poll = get_object_or_404(Poll, pk=pk)
    if request.user != poll.owner:
        return HttpResponseRedirect(reverse('forum:detailgroup', args=[group]))
    
    poll.delete()
    return HttpResponseRedirect(reverse('forum:detailgroup', args=[group]))


@login_required
def add_choice(request, pk, group):
    poll = get_object_or_404(Poll, pk=pk)
    if request.user != poll.owner:
        return HttpResponseRedirect(reverse('polls:editpoll', args=[pk,group]))

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            return HttpResponseRedirect(reverse('polls:editpoll', args=[pk,group]))

@login_required
def choice_edit(request, choice_id, group):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            return redirect('polls:editpoll', poll.pk, group)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_delete(request, choice_id, group):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')
    choice.delete()
    return redirect('polls:editpoll', poll.pk, group)


def poll_detail(request, pk, group):
    poll = get_object_or_404(Poll, id=pk)

    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/poll_detail.html', context)


@login_required
def poll_vote(request, pk, group):
    poll = get_object_or_404(Poll, pk=pk)
    choice_id = request.POST.get('choice')

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        return HttpResponseRedirect(reverse('forum:detailgroup', args=[group]))
    else:
        return redirect("polls:detailpoll", pk, group)

