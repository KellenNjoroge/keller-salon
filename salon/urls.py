from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name = 'index'),
    url('profile/$', views.profile, name='profile'),
    url('update/$', views.update, name='update'),
    url('^new_town/$', views.new_town, name='new_town'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
