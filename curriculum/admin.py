from django.contrib import admin
from mentortogether.curriculum.models import Curriculum
from mentortogether.curriculum.models import CurriculumSection
from mentortogether.curriculum.models import CurriculumPrompt


class CurriculumAdmin(admin.ModelAdmin):
    ordering = ('title',)


class CurriculumSectionAdmin(admin.ModelAdmin):
    list_display       = ('curriculum', 'title')
    list_display_links = ('title',)
    list_filter        = ('curriculum',)
    ordering           = ('curriculum', 'rank')
    exclude            = ('edit_date', 'edit_by', 
                          'create_date', 'create_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_by = request.user
        obj.edit_by   = request.user
        obj.save()

class CurriculumPromptAdmin(admin.ModelAdmin):
    list_display       = ('curriculum', 'section', 'title')
    list_display_links = ('section', 'title')
    list_filter        = ('section',)
    ordering           = ('section', 'rank')
    exclude            = ('edit_date', 'edit_by', 
                          'create_date', 'create_by')

    def curriculum(self, obj):
        return obj.section.curriculum

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_by = request.user
        obj.edit_by   = request.user
        obj.save()

admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(CurriculumSection, CurriculumSectionAdmin)
admin.site.register(CurriculumPrompt, CurriculumPromptAdmin)
