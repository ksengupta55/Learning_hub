from django.contrib import admin
from .models import Lesson, Category

# Register your models here.
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'keywords', 'submitted',)
    list_filter = ('submitted', 'createdby')
    readonly_fields = ('submitted',)
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'keywords',)
        }),
        ('Problem Statement', {
            'classes': ('collapse',),
            'fields': ('problem_statement',),
        }),
        ('Lesson Creator', {
            'classes': ('collapse',),
            'fields': ('createdby',),
        }),
        ('Submission Information', {
            'classes': ('collapse',),
            'fields': ('problem_document', 'submitted',),
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    #readonly_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )


# Register your models here.
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Category, CategoryAdmin)


