from django.shortcuts import render, redirect, get_object_or_404
from .models import Establishment, Review, User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import UserRegistrationForm, UserLoginForm, EstablishmentForm, ReviewForm
from django.db.models import Avg, Count
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

def admin_est_list(request):
    establishments = Establishment.objects.all()
    query = request.GET.get('search')
    if query:
        establishments = establishments.filter(name__icontains=query)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'rating':
        establishments = establishments.order_by('-average_rating')
    return render(request, 'admin_page.html', {'establishments': establishments})

def admin_est_detail(request, establishment_id):
    establishment = get_object_or_404(Establishment, id=establishment_id)
    reviews = Review.objects.filter(establishment=establishment)
    return render(request, 'admin_est_detail.html', {'establishment': establishment, 'reviews': reviews})


def edit_est_info(request, establishment_id):
    establishment = get_object_or_404(Establishment, pk=establishment_id)

    if request.method == 'POST':
        form = EstablishmentForm(request.POST, instance=establishment)
        if form.is_valid():
            form.save()
            return redirect('admin_est_detail', establishment_id=establishment_id)
    else:
        form = EstablishmentForm(instance=establishment)

    return render(request, 'edit_est_info.html', {'form': form, 'establishment': establishment})

def establishment_detail(request, establishment_id):
    establishment = get_object_or_404(Establishment, id=establishment_id)
    reviews = Review.objects.filter(establishment=establishment)
    return render(request, 'establishment_detail.html', {'establishment': establishment, 'reviews': reviews})


def add_review(request, establishment_id):
    establishment = get_object_or_404(Establishment, pk=establishment_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.establishment = establishment
            review.save()

            # Обновление среднего рейтинга заведения
            establishment_reviews = Review.objects.filter(establishment=establishment)
            establishment_average_rating = establishment_reviews.aggregate(Avg('rating'))['rating__avg']
            establishment.average_rating = establishment_average_rating
            establishment.save()

            return redirect('establishment_detail', establishment_id=establishment_id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'establishment': establishment})


def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('establishment_detail', establishment_id=review.establishment.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})


def create_establishment(request):
    if request.method == 'POST':
        form = EstablishmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('establishment_list')
    else:
        form = EstablishmentForm()
    return render(request, 'create_establishment.html', {'form': form})

def delete_establishment(request, establishment_id):
    establishment = get_object_or_404(Establishment, pk=establishment_id)

    if request.method == 'POST':
        establishment.delete()
        return redirect('establishment_list')

    return render(request, 'confirm_delete_establishment.html', {'establishment': establishment})




def user_profile(request):
    user_reviews = Review.objects.filter(user=request.user)

    establishment_reviews = {}

    for review in user_reviews:
        establishment_name = review.establishment.name
        if establishment_name not in establishment_reviews:
            establishment_reviews[establishment_name] = []
        establishment_reviews[establishment_name].append(review)

    return render(request, 'user_profile.html', {'establishment_reviews': establishment_reviews})



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


