import os
import debug_toolbar

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('accounts/', include('registration.backends.admin_approval.urls')),
    path('accounts/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('', include('experiment.urls')),
]

if os.getenv('PRODUCTION'):
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
