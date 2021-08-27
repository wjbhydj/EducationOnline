import xadmin
from .models import UserAsk, UserCourse, UserFavorite, UserMessage, CourseComments

class UserAskXadmin(object):

    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class UserCourseXadmin(object):

    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']


class UserFavoriteXadmin(object):

    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class UserMessageXadmin(object):

    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class CourseCommentsXadmin(object):

    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments', 'add_time']
    list_filter = ['user', 'course', 'comments', 'add_time']


xadmin.site.register(UserAsk, UserAskXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)
xadmin.site.register(UserFavorite, UserFavoriteXadmin)
xadmin.site.register(UserMessage, UserMessageXadmin)
xadmin.site.register(CourseComments,CourseCommentsXadmin)