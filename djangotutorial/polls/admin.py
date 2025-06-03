from django.contrib import admin
from django.urls import path
from .models import Choice, Question
from .views import admin_view
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Candidate

class MyAdminSite(admin.AdminSite):
    site_header = "Administrácia Webovej stránky"
    site_title = "Admin Portal"
    index_title = "Prístup povolený len daným používateľom"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin_view/', self.admin_view, name='admin_view'),
        ]
        return custom_urls + urls

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

admin_site = MyAdminSite(name="myadmin")
admin.site = admin_site
admin.site.register(Question, QuestionAdmin)
admin.site.register(Candidate)
admin_site.register(User, UserAdmin)