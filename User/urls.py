__author__ = 'Roden Magat'
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from User import views
from rest_framework import routers
router = routers.SimpleRouter()

urlpatterns = format_suffix_patterns([
    url(r'^user_list/$', views.UserCrudViewSet.as_view({ 'get': 'list' }), name='user-list'),
    url(r'^user_create/$', views.UserCrudViewSet.as_view({ 'post': 'create' }), name='user-create'),
    url(r'^user_update/(?P<pk>.+)/$', views.UserCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='user-put'),
    url(r'^user_delete/(?P<pk>.+)/$', views.UserCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='user-delete'),

    url(r'^user_simple_update/(?P<pk>.+)/$', views.SimpleUserCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='user-put'),

    url(r'^group_list/$', views.GroupViewSet.as_view({ 'get': 'list' }), name='group-list'),
    url(r'^group_create/$', views.GroupViewSet.as_view({ 'post': 'create' }), name='group-create'),
    url(r'^group_update/(?P<pk>.+)/$', views.GroupViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='group-put'),
    url(r'^group_delete/(?P<pk>.+)/$', views.GroupViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='group-delete'),
])

urlpatterns += [
    url(r'^user_app/', include(router.urls)),
]
