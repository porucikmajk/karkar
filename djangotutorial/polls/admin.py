from django.contrib import admin
from .models import Choice, Question

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

def reset_voters(modeladmin, request, queryset):
    for question in queryset:
        for choice in question.choice_set.all():
            choice.voters.clear()
            choice.votes = 0
            choice.save()
    modeladmin.message_user(request, "Voters have been reset.")

reset_voters.short_description = "Reset voters"

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "question", "votes"]

admin.site.register(Question, QuestionAdmin)
