from django.contrib import admin
from models import Project, WritingPrompt, Mentorship, Message

class ProjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Project, ProjectAdmin)

class WritingPromptAdmin(admin.ModelAdmin):
    pass
admin.site.register(WritingPrompt, WritingPromptAdmin)

class MentorshipAdmin(admin.ModelAdmin):
    list_display = ['mentor_app', 'mentee_app' ]
    ordering     = ['mentor_app']

admin.site.register(Mentorship, MentorshipAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'subject', 'senton' ]

admin.site.register(Message, MessageAdmin)

