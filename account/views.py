from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from common.decorators import ajax_required
from tweets.models import Tweet, Like, Dislike
from twitter.settings import EMAIL_HOST_USER
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact

def main(request):
    return redirect('login')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Аутентификация успешна')
            else:
                return HttpResponse('аккаунт неактивен')
        else:
            return HttpResponse('Неправильный логин')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    user = request.user
    tweets = Tweet.objects.filter(user=user)
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'user': user,
                   'tweets': tweets})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter()
    users = users.exclude(id=request.user.id)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users,
                   'title': 'Люди', })


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    tweets = Tweet.objects.filter(user=user)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user,
                   'tweets': tweets, })


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


@login_required
def followers_list(request):
    followers = request.user.followers.all()
    return render(request,
                  'account/user/list.html',
                  {'users': followers,
                   'title': 'Подписчики', })


@login_required
def following_list(request):
    following = request.user.following.all()
    return render(request,
                  'account/user/list.html',
                  {'users': following,
                   'title': 'Подписки', })


class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
    from_email = EMAIL_HOST_USER


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_complete.html'

