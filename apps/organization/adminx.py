import xadmin
from .models import CityDict, CourseOrg, Teacher

class CityDictXadmin(object):

    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgXadmin(object):

    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']


class TeacherXadmin(object):

    list_display = ['org', 'name', 'work_years', 'work_position', 'work_company', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_position', 'work_company', 'points', 'click_nums', 'fav_nums', 'add_time']
    list_filter = ['org', 'name', 'work_years', 'work_position', 'work_company', 'points', 'click_nums', 'fav_nums', 'add_time']

xadmin.site.register(CityDict, CityDictXadmin)
xadmin.site.register(CourseOrg, CourseOrgXadmin)
xadmin.site.register(Teacher, TeacherXadmin)