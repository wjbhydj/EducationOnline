from django.shortcuts import render
from django.views.generic import View
from .models import Course
from operation.models import UserFavorite
from pure_pagination import Paginator, PageNotAnInteger
# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = Course.objects.all().order_by('-click_nums')
            elif sort == 'students':
                all_courses = Course.objects.all().order_by('-students')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 2, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses':courses,
            'hot_courses':hot_courses,
            'sort':sort,
        })


class CourseDetailView(View):
    """课程详情页"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:3]
        else:
            related_courses = []
        return render(request, 'course-detail.html', {
            'course':course,
            'related_courses':related_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })
