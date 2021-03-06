from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField

# Create your models here.

class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级'),
    )
    name = models.CharField('课程名', max_length=100)
    desc = models.CharField('描述', max_length=200)
    # detail = models.TextField('详情')
    detail = UEditorField('课程详情', width=600, height=400, default='', imagePath='course/ueditor', filePath='course/ueditor')
    degree = models.CharField('难度', choices=DEGREE_CHOICES, max_length=2)
    learn_times = models.IntegerField('学习时长(分钟数)', default=0)
    students = models.IntegerField('学习人数', default=0)
    fav_nums = models.IntegerField('收藏人数', default=0)
    image = models.ImageField('封面图', upload_to='course/%Y/%m', max_length=100)
    click_nums = models.IntegerField('点击数', default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    course_org = models.ForeignKey(CourseOrg, verbose_name='所属机构', on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField('课程类别', max_length=50, default='')
    tag = models.CharField('课程标签', max_length=10, default='')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', on_delete=models.CASCADE, null=True, blank=True)
    you_need_know = models.CharField('课程须知', max_length=300, default='')
    teacher_tell_you = models.CharField('老师告诉你', max_length=300, default='')
    is_banner = models.BooleanField('是否轮播', default=False)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        """获取这门课程的章节数"""
        return self.lesson_set.all().count()
    get_zj_nums.short_description = '章节数'

    def get_learn_users(self):
        """获取这门课程的学习人数"""
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        """获取这门课程的章节"""
        return self.lesson_set.all()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField('章节名', max_length=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{}》课程的章节 >> {}'.format(self.course, self.name)

    def get_lesson_video(self):
        """获取这门章节的视频"""
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)
    name = models.CharField('视频名', max_length=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    url = models.CharField('访问地址', default='', max_length=200)
    learn_times = models.IntegerField('学习时长（分钟数）', default=0)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=100)
    download = models.FileField('资源文件', upload_to='course/%Y/%m', max_length=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

