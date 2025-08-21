from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from users.models import User
from django.contrib import auth, messages
from shop.models import Basket
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Зарегестрирование успешно завершено')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    baskets = Basket.objects.filter(user=request.user)
    # total_sum = sum(basket.sum() for basket in baskets)
    # total_quantity = sum(basket.quantity for basket in baskets)
    # total_sum = 0
    # total_quantity = 0
    # for basket in baskets:
    #      total_sum = total_sum + basket.sum()
    #      total_quantity = total_quantity + basket.quantity
    context = {'title': 'Профиль',
               'form': form,
               'baskets': baskets,
               # 'total_sum': total_sum,
               # 'total_quantity': total_quantity
               }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = get_user_model().objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Пароль успешно изменён')
                return HttpResponseRedirect(reverse('users:login'))
            except get_user_model().DoesNotExist:
                messages.error(request, 'Пользователь не найден')
        else:
            messages.error(request, 'Пароли не совпадают')

    return render(request, 'users/password_reset.html')
