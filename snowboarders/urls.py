from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse

import rest.views_user as views_user
import rest.views_chat as views_chat
import rest.views_training as views_training
from snowboarders.settings import PROJECT_PATH


def last_requests(request):
    with open(PROJECT_PATH + "../logs/requests.log", 'r') as content_file:
        content = content_file.read()
        return HttpResponse("<plaintext>"+content)

api_user_urls = [
    url(r'^users_get/$', views_user.users_get),
    url(r'^get/$', views_user.user_get),
    url(r'^login/$', views_user.login),
    url(r'^register/$', views_user.register),
]

api_chat_urls = [
    url(r'^send_message/$', views_chat.send_message),
    #url(r'^create/$', views_chat.create),
    url(r'^get_my/$', views_chat.get_my),
    url(r'^get_my_list/$', views_chat.get_my_list),
    url(r'^get_with_user/$', views_chat.get_chat_with_user),
    url(r'^get_chat_history/$', views_chat.get_chat_history),
]

api_training_urls = [
    url(r'^create/$', views_training.create),
    url(r'^get_my/$', views_training.get_my),
    url(r'^get_my_list/$', views_training.get_my_list),
    url(r'^get_list/$', views_training.get_list),
]

urlpatterns = [
    url(r'^last_requests/$', last_requests, name='last_requests'),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api/user/', include(api_user_urls)),
    url(r'^api/chat/', include(api_chat_urls)),
    url(r'^api/training/', include(api_training_urls)),
]
