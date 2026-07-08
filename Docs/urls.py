__author__ = 'Roden Magat'
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from Document import views
from rest_framework import routers
router = routers.SimpleRouter()

urlpatterns = format_suffix_patterns([
    url(r'^document_list/$', views.DocumentCrudViewSet.as_view({ 'get': 'list' }), name='document-list'),
    url(r'^document_create/$', views.DocumentCrudViewSet.as_view({ 'post': 'create' }), name='document-create'),
    url(r'^document_update/(?P<pk>.+)/$', views.DocumentCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='document-put'),
    url(r'^document_delete/(?P<pk>.+)/$', views.DocumentCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='document-delete'),
])

urlpatterns += [
    url(r'^document_app/', include(router.urls)),
]
