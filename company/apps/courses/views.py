from django.shortcuts import render
from django.views.generic import View
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operations.models import UserFav,CourseComments,UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequireMixin
# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]
        sort = request.GET.get('sort','')
        keywords=request.GET.get("keywords",'')
        active='ccourse'
        if keywords:
            all_courses = Course.objects.filter(name__icontains=keywords).order_by('-add_time')
        if sort:
            if sort=='hot':
                all_courses = all_courses.order_by('-click_nums')
            if sort=='students':
                all_courses = all_courses.order_by('-studys')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page =1
        p = Paginator(all_courses,3,request=request)

        all_courses = p.page(page)

        return render(request,'course-list.html',{
            'all_courses':all_courses,
            'sort':sort,
            'hot_courses':hot_courses,
            'keywords':keywords,
            'active':active
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        tag = course.tag
        if tag:
            tcourses = Course.objects.filter(tag=tag)[:3]
        has_course_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                has_course_fav = True
            if UserFav.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                has_org_fav = True
        active='ccourse'
        return render(request,'course-detail.html',{
            'course':course,
            'tcourses':tcourses,
            'has_org_fav':has_org_fav,
            'has_course_fav':has_course_fav,
            'active': active
        })


class CourseInfoView(LoginRequireMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        user = request.user
        try:
            if UserCourse.objects.get(course=course,user=user):
                u_course = UserCourse(course=course,user=user)
                o_course=UserCourse.objects.get(course=course,user=user)
                o_course.delete()
                u_course.save()
        except:
            u_course = UserCourse(course=course, user=user)
            u_course.save()

        #查找相关课程
        user_courses = UserCourse.objects.filter(course=course)
        user_course_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_course_ids)
                                                    #user_id字段_in  便是用户的id在这个范围中
        relate_courses = [user_course.course for user_course in all_user_courses]
        active='ccourse'
        return render(request,'course-video.html',{
            'course':course,
            'relate_courses':relate_courses,
            'active': active
        })

class CourseCommentsView(LoginRequireMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course_comments = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'course_comments':course_comments,
        })


class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id)>0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course = course
            course_comment.comment = comments
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论出错"}', content_type='application/json')