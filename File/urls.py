__author__ = 'Roden Magat'
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from File import views
from rest_framework import routers
router = routers.SimpleRouter()
from django.urls import path

urlpatterns = format_suffix_patterns([
    url(r'^document_type_list/$', views.DocumentTypeCrudViewSet.as_view({ 'get': 'list' }), name='document_type-list'),
    url(r'^document_type_create/$', views.DocumentTypeCrudViewSet.as_view({ 'post': 'create' }), name='document_type-create'),
    url(r'^document_type_update/(?P<pk>.+)/$', views.DocumentTypeCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='document_type-put'),
    url(r'^document_type_delete/(?P<pk>.+)/$', views.DocumentTypeCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='document_type-delete'),
    url(r'^document_type_option/$', views.DocumentTypeOptionViewSet.as_view({ 'get': 'list' }), name='document_type_option-list'),
    

    url(r'^document_file_list/$', views.DocumentFileCrudViewSet.as_view({ 'get': 'list' }), name='document_file-list'),
    url(r'^document_file_create/$', views.DocumentFileCrudViewSet.as_view({ 'post': 'create' }), name='document_file-create'),
    url(r'^document_file_update/(?P<pk>.+)/$', views.DocumentFileCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='document_file-put'),
    url(r'^document_file_delete/(?P<pk>.+)/$', views.DocumentFileCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='document_file-delete'),
    url(r'^document_file_view/(?P<pk>.+)/$', views.DocumentFileCrudViewSet.as_view({ 'post': 'view_document' }), name='document_file-view'),

    url(r'^document_file_list_admin/$', views.DocumentFileCrudAdminViewSet.as_view({ 'get': 'list' }), name='document_file-list_admin'),
    url(r'^document_file_create_admin/$', views.DocumentFileCrudAdminViewSet.as_view({ 'post': 'create' }), name='document_file-create_admin'),
    url(r'^document_file_update_admin/(?P<pk>.+)/$', views.DocumentFileCrudAdminViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='document_file-put_admin'),
    url(r'^document_file_delete_admin/(?P<pk>.+)/$', views.DocumentFileCrudAdminViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='document_file-delete_admin'),

    path('compare_documents/', views.CompareDocumentsView.as_view(), name='compare_documents-api'),
    path('activity/', views.ActivityView.as_view()), # background task

    #dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    #logs
    url(r'^activity_list/$', views.ActivityCrudViewSet.as_view({ 'get': 'list' }), name='activity-list'),
    url(r'^activity_create/$', views.ActivityCrudViewSet.as_view({ 'post': 'create' }), name='activity-create'),
    url(r'^activity_update/(?P<pk>.+)/$', views.ActivityCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='activity-put'),
    url(r'^activity_delete/(?P<pk>.+)/$', views.ActivityCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='activity-delete'),
])

urlpatterns += [
    url(r'^document_app/', include(router.urls)),
]
