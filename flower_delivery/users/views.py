# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm  # Импортируем нашу кастомную форму
from .models import Profile

def home(request):
    return render(request, 'users/home.html')  # Главная страница

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Используем кастомную форму
        if form.is_valid():
            user = form.save()
            # Заполняем профиль данными из формы
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.save()
            messages.success(request, f"Аккаунт был создан!")
            return redirect('login')  # Перенаправляем на страницу входа
    else:
        form = CustomUserCreationForm()  # Используем кастомную форму при GET-запросе
    return render(request, 'users/register.html', {'form': form})

                                                                                                                       

