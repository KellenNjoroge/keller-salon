from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name = 'index'),
    url('profile/$', views.profile, name='profile'),
    url('update/$', views.update, name='update'),
    url('^town/(\w+)', views.town, name='town'),
    url('^new_town/$', views.new_town, name='new_town'),
    url('^join/(\d+)', views.join, name='join'),
    url('^all_towns/$',views.all_towns,name='all_towns'),
    url('^comment/(\d+)', views.comment, name='comment'),
    url('^new_post/$', views.new_post, name='new_post'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
