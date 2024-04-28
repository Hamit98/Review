from django.urls import path
from .views import establishment_list, establishment_detail, add_review, user_profile, register, user_login, user_logout, create_establishment

urlpatterns = [
    path('', establishment_list, name='establishment_list'),
    path('establishment/<int:establishment_id>/', establishment_detail, name='establishment_detail'),
    path('establishment/<int:establishment_id>/add_review/', add_review, name='add_review'),
    path('profile/', user_profile, name='user_profile'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create_establishment/', create_establishment, name='create_establishment')
    # Другие URL-маршруты здесь
]