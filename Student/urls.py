__author__ = 'Roden Magat'
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from Student import views
from rest_framework import routers
router = routers.SimpleRouter()

urlpatterns = format_suffix_patterns([
    url(r'^student_list/$', views.StudentCrudViewSet.as_view({ 'get': 'list' }), name='student-list'),
    url(r'^student_create/$', views.StudentCrudViewSet.as_view({ 'post': 'create' }), name='student-create'),
    url(r'^student_update/(?P<pk>.+)/$', views.StudentCrudViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'patch': 'partial_update' }), name='student-put'),
    url(r'^student_delete/(?P<pk>.+)/$', views.StudentCrudViewSet.as_view({ 'get': 'retrieve', 'delete': 'destroy' }), name='student-delete'),
    url(r'^student_label_value_list/$', views.StudentLabelValueViewSet.as_view({ 'get': 'list' }), name='StudentLabelValue-list'),
    url('student_filter/', views.StudentFilterView.as_view()),
    url('student_rfid_filter/', views.StudentRFIDFilterView.as_view()),

    #autocomplete
    url(r'student_autocomplete/', views.StudentAutocompleteAPIView.as_view(), name='student-autocomplete'),
])

urlpatterns += [
    url(r'^student_app/', include(router.urls)),
]
