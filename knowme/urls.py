from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from questions import views
from profiles.views import profile_view, job_add, job_edit 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard_view, name='dashboard'),
    url(r'^question/(?P<id>\d+)/$', views.single, name='question_single'),
    url(r'^question/$', views.create_view, name='question_home'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', profile_view, name='profile'),
    url(r'^profile/job/add/$', job_add, name='job_add'),
    url(r'^profile/job/edit/$', job_edit, name='job_edit'),
]



if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
