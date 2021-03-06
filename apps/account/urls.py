from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
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
