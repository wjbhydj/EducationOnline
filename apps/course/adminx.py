import xadmin
from .models import Course, CourseResource, Video, Lesson

class CourseXadmin(object):

    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']


class CourseResourceXadmin(object):

    list_dispaly = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download', 'add_time']
    list_filter = ['course', 'name', 'download', 'add_time']


class VideoXadmin(object):

    list_display = ['lesson', 'name', 'add_time', 'url']
    search_fields = ['lesson', 'name', 'add_time', 'url']
    list_filter = ['lesson', 'name', 'add_time', 'url']


class LessonXadmin(object):

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', 'add_time']
    list_filter = ['course', 'name', 'add_time']


xadmin.site.register(Course, CourseXadmin)
xadmin.site.register(CourseResource, CourseResourceXadmin)
xadmin.site.register(Video, VideoXadmin)
xadmin.site.register(Lesson, LessonXadmin)