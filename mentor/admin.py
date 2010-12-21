from django.contrib import admin
from models import Project, WritingPrompt, Mentorship, Message, MessageThread

class ProjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Project, ProjectAdmin)

class WritingPromptAdmin(admin.ModelAdmin):
    pass
admin.site.register(WritingPrompt, WritingPromptAdmin)


class MentorshipAdmin(admin.ModelAdmin):
   list_filter  = ['project', 'curriculum']
   list_display = ['id', 'project', 'curriculum', 'mentor', 'mentee']
   ordering     = ['mentor', 'mentee']


admin.site.register(Mentorship, MentorshipAdmin)

class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ['subject', 'timestamp' ]

admin.site.register(MessageThread, MessageThreadAdmin)

