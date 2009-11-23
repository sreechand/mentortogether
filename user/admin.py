from django.contrib import admin
from mentortogether.user.models import MenteeApplication
from mentortogether.user.models import MentorApplication
from mentortogether.user.models import UserProfile, Photo

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'status']
    list_filter  = ['status' ]
    ordering     = ['status']
    actions      = ['approveApplications']

    def approveApplications(self, request, queryset):
        for app in queryset:
            app.approve()

    approveApplications.short_description = u'Approve Application(s)'


class MenteeApplicationAdmin(ApplicationAdmin):
    pass

class MentorApplicationAdmin(ApplicationAdmin):
    pass

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MenteeApplication, MenteeApplicationAdmin)
admin.site.register(MentorApplication, MentorApplicationAdmin)
admin.site.register(Photo, PhotoAdmin)
