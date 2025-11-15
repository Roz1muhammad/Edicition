
from .models import  Course, Group, GroupStudent, Interested, Dars, Davomat,Ball
from .models import User
from django.contrib import admin
from .models import Ball
from .forms import BallForm

@admin.register(Ball)
class BallAdmin(admin.ModelAdmin):
    form = BallForm
    list_display = ["oquvchi", "oqtuvchi", "group", "ball"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone",  "is_active", "is_staff", "is_superuser")
    search_fields = ("username",)
    list_filter = ("ut", "is_active", "is_staff")


# Qolgan adminlar xuddi shunday...
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "mentor")
    search_fields = ("name", "mentor__username")
    list_filter = ("mentor",)
    ordering = ("name",)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "duration", "status", "start_date")
    list_filter = ("status", "course")
    search_fields = ("name", "course__name")
    list_editable = ("status",)
    ordering = ("-start_date",)

@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = ("student", "group", "start_date", "end_date")
    list_filter = ("group",)
    search_fields = ("student__username", "group__name")
    autocomplete_fields = ("student", "group")
    ordering = ("-start_date",)

@admin.register(Interested)
class InterestedAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "telegram", "via", "view", "contacted", "who_contacted")
    list_filter = ("contacted", "view", "via")
    search_fields = ("name", "phone", "telegram")
    list_editable = ("contacted", "view")
    readonly_fields = ("who_contacted",)
    ordering = ("-id",)

@admin.register(Dars)
class DarsAdmin(admin.ModelAdmin):
    list_display = ("topic", "group", "startedTime", "endedTime", "is_end", "created")
    list_filter = ("group", "is_end")
    search_fields = ("topic", "group__name")
    date_hierarchy = "startedTime"
    list_editable = ("is_end",)
    ordering = ("-startedTime",)

@admin.register(Davomat)
class DavomatAdmin(admin.ModelAdmin):
    list_display = ("dars", "group", "user", "status", "created")
    list_filter = ("status", "group", "dars")
    search_fields = ("user__username", "dars__topic", "group__name")
    list_editable = ("status",)
    date_hierarchy = "created"
    ordering = ("-created",)



