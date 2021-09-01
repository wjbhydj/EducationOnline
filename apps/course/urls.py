from django.conf.urls import url
from . import views

app_name = 'course'

urlpatterns = [
    url('list/', views.CourseListView.as_view(), name='course_list'),
    url('detail/(?P<course_id>\d+)/', views.CourseDetailView.as_view(), name='course_detail'),
]