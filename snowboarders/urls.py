from django.conf.urls import url, include
from django.contrib import admin
import rest.views_user as views_user
import rest.views_chat as views_chat

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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api/user/', include(api_user_urls)),
    url(r'^api/chat/', include(api_chat_urls)),
]
