import xadmin
from .models import UserAsk,UserMessage,CourseComments,UserCourse,UserFav

class UserAskAdmin(object):
    list_display=('name','moblie','course','add_time')
    search_fields=('name','moblie','course')
    list_filter=('name','moblie','course')

class UserMessageAdmin(object):
    list_display=('user','has_read','add_time')
    search_fields=('user','has_read')
    list_filter=('user','has_read')

class CourseCommentsAdmin(object):
    list_display=('user','course','add_time')
    search_fields=('user__name','course__name')
    list_filter=('user','course')

class UserCourseAdmin(object):
    list_display=('user','course','add_time')
    search_fields=('user__name','course__name')
    list_filter=('user','course')

class UserFavAdmin(object):
    list_display = ('user', 'fav_type', 'add_time')
    search_fields = ('user_name', 'fav_type')
    list_filter = ('user', 'fav_type')
xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserFav,UserFavAdmin)



