from django.conf.urls import url
from . import views

app_name = 'course'

urlpatterns = [
    url('list/', views.CourseListView.as_view(), name='course_list'),
    url('detail/(?P<course_id>\d+)/', views.CourseDetailView.as_view(), name='course_detail'),
    url('info/(?P<course_id>\d+)/', views.CourseInfoView.as_view(), name='course_info'),
    url('comment/(?P<course_id>\d+)/', views.CourseCommentView.as_view(), name='course_comment'),
    url('add_comment/', views.AddCommentView.as_view(), name='add_comment'),
    url('video/(?P<video_id>\d+)/', views.VideoPlayView.as_view(), name='video_play'),
]