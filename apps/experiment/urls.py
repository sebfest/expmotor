from django.urls import path, re_path

from experiment import views

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
        'experiment/<int:pk>/session/add/',
        views.SingleSessionCreateView.as_view(),
        name='session_add'
    ),
    path(
        'experiment/<int:pk>/session/add_multiple/',
        views.MultipleSessionCreateView.as_view(),
        name='session_add_multiple'
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
        'experiment/<int:pk>/participants/',
        views.ParticipantListView.as_view(),
        name='participant_list'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk>/partcipant/add/',
        views.ParticipantCreateView.as_view(),
        name='participant_add'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk_ses>/participant/<int:pk>/update/',
        views.ParticipantUpdateView.as_view(),
        name='participant_update'
    ),
    path(
        'experiment/<int:pk_eks>/session/<int:pk_ses>/participant/<int:pk>/delete/',
        views.ParticipantDeleteView.as_view(),
        name='participant_delete'
    ),
    path(
        'experiment/<int:pk>/register/',
        views.RegistrationView.as_view(),
        name='registration_create'
    ),
    path(
        'experiment/<int:pk>/register/success',
        views.RegistrationPreConfirmView.as_view(),
        name='registration_success'
    ),
    re_path(
        r'^experiment/register/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
        views.RegistrationActivateView.as_view(),
        name='registration_activate'
    ),
    path(
        'experiment/register/confirm',
        views.RegistrationPostConfirmView.as_view(),
        name='registration_confirm'
    ),
]
