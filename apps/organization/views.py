from django.shortcuts import render
from django.views.generic.base import View
from .models import CityDict, CourseOrg
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse
from .forms import UserAskForm
from operation.models import UserFavorite

# Create your views here.

class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by(('course_nums'))
        org_onums = all_orgs.count()
        all_citys = CityDict.objects.all()

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs':orgs,
            'org_onums':org_onums,
            'all_citys':all_citys,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })


class AddUserAskView(View):

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse({'status':'success'}, content_type='application/json')
        else:
            return HttpResponse({'status':'fail', 'msg':'添加失败'}, content_type='application/json')


class OrgHomeView(View):

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:4]
        all_teachers = course_org.teacher_set.all()[:2]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html',
                      {
                          'course_org':course_org,
                          'all_courses':all_courses,
                          'all_teachers':all_teachers,
                          'current_page':current_page,
                          'has_fav':has_fav,
                      })


class OrgCourseView(View):
    """机构课程列表页"""
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'course_org':course_org,
            'all_courses':all_courses,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgDescView(View):
    """机构描述页"""
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'current_page':current_page,
            'course_org':course_org,
            'has_fav':has_fav,
        })

class OrgTeacherView(View):
    """机构教师页"""
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'current_page':current_page,
            'course_org':course_org,
            'all_teachers':all_teachers,
            'has_fav':has_fav,
        })

class AddFavView(View):
    """收藏"""
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated:
            return HttpResponse({'status':'fail','msg':'用户未登录'}, content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            exist_record.delete()
            return HttpResponse({'status':'success','msg':'收藏'}, content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse({'status':'success','msg':'已收藏'}, content_type='application/json')
            else:
                return HttpResponse({'status':'fail', 'msg':'收藏出错'}, content_type='application/json')