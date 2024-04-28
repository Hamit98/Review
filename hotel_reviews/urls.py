from django.urls import path
from reviews.views import establishment_list, delete_establishment, edit_est_info, admin_est_detail, admin_est_list, establishment_detail, add_review, user_profile, register, user_login, user_logout, create_establishment

urlpatterns = [
    path('', establishment_list, name='establishment_list'),
    path('admin_page/', admin_est_list, name='admin_page'),
    path('admin_est_detail/<int:establishment_id>/', admin_est_detail, name='admin_est_detail'),
    path('edit_est_info/<int:establishment_id>/', edit_est_info, name='edit_est_info'),
    path('delete_est/<int:establishment_id>/', delete_establishment, name='delete_establishment'),
    path('establishment/<int:establishment_id>/', establishment_detail, name='establishment_detail'),
    path('establishment/<int:establishment_id>/add_review/', add_review, name='add_review'),
    path('profile/', user_profile, name='user_profile'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create_establishment/', create_establishment, name='create_establishment')
    # Другие URL-маршруты здесь
]
