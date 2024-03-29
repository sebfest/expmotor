from django.urls import path, re_path

from . import views

app_name = 'experiment'
urlpatterns = [
    path(
        '',
        views.ExperimentListView.as_view(),
        name='experiment_list'
    ),
    path(
        'experiment/add/',
        views.ExperimentCreateView.as_view(),
        name='experiment_add'
    ),
    path(
        'experiment/<int:pk>/',
        views.ExperimentDetailView.as_view(),
        name='experiment_detail'
    ),
    path(
        'experiment/<int:pk>/update/',
        views.ExperimentUpdateView.as_view(),
        name='experiment_update'
    ),
    path(
        'experiment/<int:pk>/delete/',
        views.ExperimentDeleteView.as_view(),
        name='experiment_delete'
    ),
    path(
        'experiment/<int:pk>/qrcode/',
        views.ExperimentQrcodeDownloadView.as_view(),
        name='experiment_qr_download'
    ),
    path(
        'experiment/<int:pk>/printout/',
        views.ExperimentPrintoutDownloadView.as_view(),
        name='experiment_printout_download'
    ),
    path(
        'experiment/<int:pk>/session/add/',
        views.SessionCreateView.as_view(),
        name='session_add'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk>/',
        views.SessionDetailView.as_view(),
        name='session_detail'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk>/update/',
        views.SessionUpdateView.as_view(),
        name='session_update'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk>/delete/',
        views.SessionDeleteView.as_view(),
        name='session_delete'
    ),
    path(
        'experiment/<int:pk>/registrations/',
        views.RegistrationListView.as_view(),
        name='registration_list'
    ),
    path(
        'experiment/<int:pk>/registrations/search/',
        views.RegistrationSearchView.as_view(),
        name='registration_search'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk>/registration/add/',
        views.RegistrationCreateView.as_view(),
        name='registration_add'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk_ses>/registration/<int:pk>/update/',
        views.RegistrationUpdateView.as_view(),
        name='registration_update'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk_ses>/registration/<int:pk>/delete/',
        views.RegistrationDeleteView.as_view(),
        name='registration_delete'
    ),
    path(
        'experiment/<int:pk>/register/',
        views.RegistrationView.as_view(),
        name='registration_create'
    ),
    path(
        'experiment/<int:pk>/register/success/',
        views.RegistrationPreConfirmView.as_view(),
        name='registration_success'
    ),
    re_path(
        r'^experiment/register/activate/(?P<uidb64>[\dA-Za-z_\-]+)/(?P<token>[\dA-Za-z]{1,6}-[\dA-Za-z]{1,32})/$',
        views.RegistrationActivateView.as_view(),
        name='registration_activate'
    ),
    path(
        'experiment/register/confirm/',
        views.RegistrationPostConfirmView.as_view(),
        name='registration_confirm'
    ),
    path(
        'about/',
        views.AboutView.as_view(),
        name='about'
    ),
    path(
        'license/',
        views.LicenseView.as_view(),
        name='license'
    ),
]
