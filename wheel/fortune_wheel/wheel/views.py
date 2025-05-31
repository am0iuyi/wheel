from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
from .models import Profile, ShopItem, Purchase
from .forms import RegisterForm, LoginForm
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'wheel/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('wheel')
    else:
        form = RegisterForm()
    return render(request, 'wheel/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('wheel')
    else:
        form = LoginForm()
    return render(request, 'wheel/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def wheel_view(request):
    return render(request, 'wheel/wheel.html')


@csrf_exempt
@login_required
def spin_wheel(request):
    if request.method == 'POST':
        try:
            user = request.user
            profile = user.profile

            # Получаем значение выигрыша из запроса
            win_amount = int(request.POST.get('win_amount', 0))

            # Обновляем статистику
            profile.games_played += 1
            profile.coins += win_amount

            if win_amount > 10:
                profile.wins += 1

            profile.save()

            return JsonResponse({
                'win': win_amount,
                'total_coins': profile.coins
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def profile_view(request):
    profile = request.user.profile
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'wheel/profile.html', {'profile': profile, 'purchases': purchases})


@login_required
def shop_view(request):
    items = ShopItem.objects.all()
    return render(request, 'wheel/shop.html', {'items': items})


@login_required
def buy_item(request, item_id):
    if request.method == 'POST':
        item = ShopItem.objects.get(id=item_id)
        profile = request.user.profile

        if profile.coins >= item.price:
            profile.coins -= item.price
            profile.save()

            Purchase.objects.create(user=request.user, item=item)
            return JsonResponse({'success': True, 'new_balance': profile.coins})
        else:
            return JsonResponse({'success': False, 'error': 'Недостаточно монет'})
    return JsonResponse({}, status=400)
