import xadmin
from .models import Course, CourseResource, Video, Lesson

class LessonInline(object):
    model = Lesson
    extra = 0

class CourseXadmin(object):

    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time', 'get_zj_nums']
    search_fields = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    model_icon = "fa fa-book"
    readonly_fields = ['click_nums']
    order_by = ['-click_nums']
    exclude = ['fav_nums']
    list_editable = ['desc', 'degree']
    inlines = [LessonInline,]
    refresh_times = [3, 5]

    style_fields = {'detail':'ueditor'}

    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

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