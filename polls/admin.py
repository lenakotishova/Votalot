from django.contrib import admin
from .models import Question, Choice, Comment


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'likes']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Author', {'fields': ['author']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'created_date', 'pub_date', 'was_published_recently', 'author_id')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Comment)