from django.urls import path

from account import views

app_name = 'account'
urlpatterns = [
    path(
        'login/',
        views.MyLoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        views.MyLogoutView.as_view(),
        name='logout',
    ),
    path(
        'register/',
        views.MySignUpView.as_view(),
        name='register',
    ),
    path(
        'profile/<int:pk>/',
        views.MyProfileDetailView.as_view(),
        name='profile_detail',
    ),
    path(
        'profile/<int:pk>/update/',
        views.MyProfileUpdateView.as_view(),
        name='profile_update',
    ),
    path(
        'profile/<int:pk>/delete/',
        views.MyProfileDeleteView.as_view(),
        name='profile_delete',
    ),
    path(
        'profile/deleted/',
        views.MyProfileDeleteDoneView.as_view(),
        name='profile_delete_success',
    ),
]
