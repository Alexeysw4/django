from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy

from tweets.forms import TweetForm
from tweets.models import Tweet, Like, Dislike


@login_required
def tweet_create(request):
    if request.method == 'POST':
        tweet_form = TweetForm(request.POST)
        if tweet_form.is_valid():
            Tweet.objects.create(text=tweet_form.cleaned_data['text'], user=request.user)
            messages.success(request, 'Tвит добавлен успешно')
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        tweet_form = TweetForm()
    return render(request, 'tweets/tweet/create.html', {'tweet_form': tweet_form})


def tweet_detail(request, id):
    tweet = get_object_or_404(Tweet, id=id)
    return render(request,
                  'tweets/tweet/detail.html',
                  {'section': 'tweets',
                   'tweet': tweet, })


@login_required
def tweet_list(request):
    tweets = Tweet.objects.order_by('-pub_date').all()
    if request.is_ajax():
        return render(request,
                      'tweets/tweet/list_ajax.html',
                      {'section': 'tweets',
                       'tweets': tweets})
    return render(request,
                  'tweets/tweet/list.html',
                  {'section': 'tweets',
                   'tweets': tweets})


@login_required
def delete(request, id):
    try:
        person = Tweet.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect(reverse('dashboard'))
    except Tweet.DoesNotExist:
        return HttpResponse("Нет такого поста")


@login_required
def add_reply(request, id):
    if request.method == 'POST':
        tweet_form = TweetForm(request.POST)
        if tweet_form.is_valid():
            Tweet.objects.create(text=tweet_form.cleaned_data['text'],
                                 user=request.user,
                                 reply_to=Tweet.objects.get(id=id))
            messages.success(request, 'Комент добавлен успешно')
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        tweet_form = TweetForm()
    return render(request, 'tweets/tweet/create.html', {'tweet_form': tweet_form})


@login_required
def like(request, pk):
    if Like.objects.filter(post_id=pk, user=request.user).exists():
        Like.objects.get(post_id=pk, user=request.user).delete()
    else:
        if Dislike.objects.filter(post_id=pk, user=request.user).exists():
            Dislike.objects.get(post_id=pk, user=request.user).delete()
        Like.objects.create(post_id=pk, user=request.user)
    return redirect('tweets:detail', pk)


@login_required
def dislike(request, pk):
    if Dislike.objects.filter(post_id=pk, user=request.user).exists():
        Dislike.objects.get(post_id=pk, user=request.user).delete()
    else:
        if Like.objects.filter(post_id=pk, user=request.user).exists():
            Like.objects.get(post_id=pk, user=request.user).delete()
        Dislike.objects.create(post_id=pk, user=request.user)
    return redirect('tweets:detail', pk)
