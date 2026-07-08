__author__ = 'Roden Magat'
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from User import views
from rest_framework import routers
router = routers.SimpleRouter()
from django.urls import path
from User import group_uploader_views

urlpatterns = format_suffix_patterns([
    url('group_upload_csv/', group_uploader_views.GroupCSVUploadViewSet.as_view({'post': 'create'})),

    url(r'^user_list/$', views.UserCrudViewSet.as_view({ 'get': 'list' }), name='user-list'),
    url(r'^user_create/$', views.UserCrudViewSet.as_view({ 'post': 'create' }), name='user-create'),
    url(r'^user_update/(?P<pk>.+)/$', views.UserCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='user-put'),
    url(r'^user_delete/(?P<pk>.+)/$', views.UserCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='user-delete'),
    url(r'^user_simple_update/(?P<pk>.+)/$', views.SimpleUserCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='user-put'),
    url('user_data_filter/', views.UserDataFilterView.as_view()),

    url(r'user_approver_autocomplete/', views.UserApproverAutocompleteIDAPIView.as_view(), name='user-autocomplete-approver'),

    url(r'^group_list/$', views.GroupViewSet.as_view({ 'get': 'list' }), name='group-list'),
    url(r'^group_create/$', views.GroupViewSet.as_view({ 'post': 'create' }), name='group-create'),
    url(r'^group_update/(?P<pk>.+)/$', views.GroupViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='group-put'),
    url(r'^group_delete/(?P<pk>.+)/$', views.GroupViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='group-delete'),

    url(r'^branch_list/$', views.BranchCrudViewSet.as_view({ 'get': 'list' }), name='brnc-list'),
    url(r'^branch_create/$', views.BranchCrudViewSet.as_view({ 'post': 'create' }), name='brnc-create'),
    url(r'^branch_update/(?P<pk>.+)/$', views.BranchCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='brnc-put'),
    url(r'^branch_delete/(?P<pk>.+)/$', views.BranchCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='brnc-delete'),

    url(r'^department_list/$', views.DepartmentCrudViewSet.as_view({ 'get': 'list' }), name='dprt-list'),
    url(r'^department_create/$', views.DepartmentCrudViewSet.as_view({ 'post': 'create' }), name='dprt-create'),
    url(r'^department_update/(?P<pk>.+)/$', views.DepartmentCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='dprt-put'),
    url(r'^department_delete/(?P<pk>.+)/$', views.DepartmentCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='dprt-delete'),

    url(r'user_autocomplete_id/', views.UserAutocompleteIDAPIView.as_view(), name='user-autocomplete'),
    url(r'branch_autocomplete/', views.BranchAutocompleteAPIView.as_view(), name='branch-autocomplete'),
    url(r'department_autocomplete/', views.DepartmentAutocompleteAPIView.as_view(), name='department-autocomplete'),
    url(r'group_autocomplete/', views.GroupAutocompleteAPIView.as_view(), name='group-autocomplete'),

    url('user_filter/', views.UserFilterView.as_view()),
    url('branch_filter/', views.BranchFilterView.as_view()),
    url('department_filter/', views.DepartmentFilterView.as_view()),
    url('group_filter/', views.GroupFilterView.as_view()),

    url(r'^main_group_list/$', views.GroupGoogleViewSet.as_view({ 'get': 'list' }), name='group-list'),
    url(r'^main_group_create/$', views.GroupGoogleViewSet.as_view({ 'post': 'create' }), name='group-create'),
    url(r'^main_group_update/(?P<pk>.+)/$', views.GroupGoogleViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='group-put'),
    url(r'^main_group_delete/(?P<pk>.+)/$', views.GroupGoogleViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='group-delete'),
    #url(r'^document_type_option/$', views.DocumentTypeOptionViewSet.as_view({ 'get': 'list' }), name='document_type_option-list'),
    
    #url(r'^group_email_list/$', views.GroupEmailViewSet.as_view({ 'get': 'list' }), name='group_email-list'),
    #url(r'^group_email_create/$', views.GroupEmailViewSet.as_view({ 'post': 'create' }), name='group_email-create'),
    #url(r'^group_email_update/(?P<pk>.+)/$', views.GroupEmailViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='group_email-put'),
    #url(r'^group_email_delete/(?P<pk>.+)/$', views.GroupEmailViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='group_email-delete'),
    #url('group_email_filter/', views.GroupEmailFilterView.as_view()),
    #url(r'^document_type_option/$', views.DocumentTypeOptionViewSet.as_view({ 'get': 'list' }), name='document_type_option-list'),


    url(r'^group_user_list/$', views.GroupUserViewSet.as_view({ 'get': 'list' }), name='group_user-list'),
    url(r'^group_user_create/$', views.GroupUserViewSet.as_view({ 'post': 'create' }), name='group_user-create'),
    url(r'^group_user_update/(?P<pk>.+)/$', views.GroupUserViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='group_user-put'),
    url(r'^group_user_delete/(?P<pk>.+)/$', views.GroupUserViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='group_user-delete'),
    url('group_user_content_filter/', views.GroupUserFilterView.as_view(), name='group_user-filtering'),
])

urlpatterns += [
    url(r'^user_app/', include(router.urls)),
]
