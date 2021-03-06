from django.shortcuts import render
from django.views.generic import View
from organizations.models import CityDict,CourseOrg,Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskFrom
from django.http import HttpResponse
from operations.models import UserFav
# Create your views here.


class OrgList(View):
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        keywords=request.GET.get("keywords",'')
        if keywords:
            all_orgs = CourseOrg.objects.filter(name__icontains=keywords)
        all_citys = CityDict.objects.all()
        big_orgs = all_orgs.order_by('-click_nums')[:3]
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
                                    #取外键值 外键_字段
        category = request.GET.get('ct','')
        if category:
            all_orgs = all_orgs.filter(category=category)
        sort = request.GET.get('sort','')
        if sort:
            if sort=='students':
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by("-courses")

        all_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,4,request=request)

        all_orgs = p.page(page)
        active='oorg'
        return render(request,"org-list.html",{
            'all_orgs':all_orgs,
            'all_citys':all_citys,
            'all_nums':all_nums,
            'city_id':city_id,
            'category':category,
            'sort':sort,
            'big_orgs':big_orgs,
            'keywords':keywords,
            'active':active
        })


class UserAskFormView(View):
    def post(self,request):
        userask_form=UserAskFrom(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success","msg":"提交成功"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"提交失败"}', content_type='application/json')
# ModelForm 直接通过表单Form将数据保存到数据库


class OrgHomeView(View):
    def get(self,request,org_id):
        # org_id=request.GET.get('org_id','')
        course_org=CourseOrg.objects.get(id=int(org_id))
        courses=course_org.course_set.all()[:2]
                         #获取机构下的所有课程,_set外键的反向获取
        teachers=course_org.teacher_set.all()[:3]
        current_page = 'home'
        org_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user,fav_id=int(org_id),fav_type=2):
                org_fav=True
        return render(request,"org-detail-homepage.html",{
            "courses":courses,
            "teachers":teachers,
            "course_org":course_org,
            "org_id":org_id,
            'current_page': current_page,
            'org_fav': org_fav,
        })


class OrgCourseView(View):
    def get(self,request,org_id):
        #org_id = request.GET.get('org_id','')
        course_org = CourseOrg.objects.get(id=int(org_id))
        courses = course_org.course_set.all()
        current_page = 'course'
        org_fav = False
        if UserFav.objects.filter(fav_id=int(org_id), fav_type=2):
            org_fav = True
        return render(request,'org-detail-course.html',{
            'courses':courses,
            'course_org':course_org,
            'org_id': org_id,
            'current_page': current_page,
            'org_fav':org_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        # org_id = request.GET.get('org_id','')
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'desc'
        org_fav = False
        if UserFav.objects.filter(fav_id=int(org_id), fav_type=2):
            org_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'org_id': org_id,
            'current_page': current_page,
            'org_fav':org_fav
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        # org_id = request.GET.get('org_id','')
        course_org = CourseOrg.objects.get(id=int(org_id))
        teachers = course_org.teacher_set.all()
        current_page = 'teacher'
        org_fav = False
        if UserFav.objects.filter( fav_id=int(org_id), fav_type=2):
            org_fav = True
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'org_id': org_id,
            'teachers':teachers,
            'current_page': current_page,
            'org_fav':org_fav
        })


class UserFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        #即便用户不登录，请求中也有user,
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFav.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFav()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teachers=Teacher.objects.all()
        keywords=request.GET.get("keywords",'')
        if keywords:
            all_teachers = all_teachers.filter(name__icontains=keywords)
        all_teachers_nums=all_teachers.count()
        sort=request.GET.get('sort','')
        if sort=='hot':
            all_teachers=all_teachers.order_by('-click_nums')
        pteachers=all_teachers.order_by('-click_nums')[:5]
        try:
            page=request.GET.get('page',1)
        except PageNotAnInteger:
            page=1
        p=Paginator(all_teachers,3,request=request)
        all_teachers=p.page(page)
        active='tteacher'
        return render(request,'teachers-list.html',{
            'all_teachers':all_teachers,
            'sort':sort,
            'pteachers':pteachers,
            'all_teachers_nums':all_teachers_nums,
            'keywords':keywords,
            'active':active
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher=Teacher.objects.get(id=int(teacher_id))
        all_teachers=Teacher.objects.all()
        pteacher=all_teachers.order_by('-click_nums')[:5]
        has_teacher_fav=False
        has_org_fav=False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user,fav_id=int(teacher_id),fav_type=3):
                has_teacher_fav=True
            if UserFav.objects.filter(user=request.user,fav_id=int(teacher_id),fav_type=2):
                has_org_fav=True
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'pteacher':pteacher,
            'has_teacher_fav':has_teacher_fav,
            'has_org_fav':has_org_fav,
        })

