from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from questions import views 
from dashboard import views as dash
from profiles.views import profile_view, job_add, job_edit 
from likes.views import like_user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', dash.dashboard_view, name='home'),
    url(r'^dashboard/$', dash.dashboard_view, name='dashboard'),
    url(r'^question/(?P<id>\d+)/$', views.single, name='question_single'),
    url(r'^like/(?P<id>\d+)/$', like_user, name='like_user'),
    url(r'^question/$', views.create_view, name='question_home'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', profile_view, name='profile'),
    url(r'^profile/job/add/$', job_add, name='job_add'),
    url(r'^profile/job/edit/$', job_edit, name='job_edit'),
    url(r'^matches/', include('matches.urls')),
]



if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
