from django.shortcuts import render, redirect, get_object_or_404
from .models import Establishment, Review, User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import UserRegistrationForm, UserLoginForm, EstablishmentForm, ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def establishment_list(request):
    establishments = Establishment.objects.all()
    query = request.GET.get('search')
    if query:
        establishments = establishments.filter(name__icontains=query)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'rating':
        establishments = establishments.order_by('-average_rating')
    return render(request, 'establishment_list.html', {'establishments': establishments})

def establishment_detail(request, establishment_id):
    establishment = get_object_or_404(Establishment, id=establishment_id)
    reviews = Review.objects.filter(establishment=establishment)
    return render(request, 'establishment_detail.html', {'establishment': establishment, 'reviews': reviews})


def add_review(request, establishment_id):
    establishment = get_object_or_404(Establishment, pk=establishment_id)

    # Получаем объект пользователя по его имени (username)
    user = get_object_or_404(User, username=request.user)
    print(user)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.establishment = establishment
            review.save()
            return redirect('establishment_detail', establishment_id=establishment_id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'establishment': establishment})
def create_establishment(request):
    if request.method == 'POST':
        form = EstablishmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('establishment_list')
    else:
        form = EstablishmentForm()
    return render(request, 'create_establishment.html', {'form': form})






def user_profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})



#Register/Autentification

def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('establishment_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('establishment_list')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('establishment_list')