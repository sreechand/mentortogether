from django.contrib import admin
from mentortogether.cms.models import Notice

class NoticeAdmin(admin.ModelAdmin):
    """
    Notice object admin interface extensions.
    """
    def save_model(self, request, obj, form, change):
        if not change:
            # Set the created-by field, if this notice
            # object is being added for the first time.
            obj.created_by = request.user
        obj.modified_by = request.user
        # This function is responsible for the final save.
        obj.save()

    # Interface Options
    list_display = ('board', 'notice_text') 

admin.site.register(Notice, NoticeAdmin)
