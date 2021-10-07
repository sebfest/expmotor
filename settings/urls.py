import os
import debug_toolbar

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('experiment.urls')),
    path('', include('account.urls')),
    path('admin/', admin.site.urls),
]

if os.getenv('PRODUCTION'):
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
