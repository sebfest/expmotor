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
]
