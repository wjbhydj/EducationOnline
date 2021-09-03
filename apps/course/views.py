from django.shortcuts import render
from django.views.generic import View
from .models import Course, Lesson, Video, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q
# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__contains=search_keywords)
                                             |Q(desc__contains=search_keywords)
                                             |Q(detail__contains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses = all_courses.order_by('-students')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
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

class CourseInfoView(LoginRequiredMixin, View):
    """课程章节视频页"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        all_recourses = CourseResource.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_courses_id.course_id for all_user_courses_id in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-video.html', {
            'course':course,
            'all_recourses':all_recourses,
            'related_courses': related_courses,
        })

class CourseCommentView(LoginRequiredMixin, View):
    """课程评论页"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_recourses = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()

        return render(request, 'course-comment.html', {
            'course':course,
            'all_recourses':all_recourses,
            'all_comments':all_comments,
        })

class AddCommentView(View):
    """添加评论"""
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse({'status':'fail', 'msg':'用户未登录'}, content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course = Course.objects.get(id=int(course_id))
            user_comment = CourseComments()
            user_comment.user = request.user
            user_comment.course = course
            user_comment.comments = comments
            user_comment.save()
            return HttpResponse({'status':'success', 'msg':'评论成功'}, content_type='application/json')
        return HttpResponse({'status':'fail', 'msg':'评论失败'}, content_type='application/json')

class VideoPlayView(LoginRequiredMixin,View):
    """课程播放"""
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_recourses = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'video':video,
            'course':course,
            'related_courses':related_courses,
            'all_recourses':all_recourses,
        })
