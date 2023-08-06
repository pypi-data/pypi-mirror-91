from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'title', 'category', 'link', 'user', 'target_user_tags', 'target_user_count', 'read_user_count', 'is_active')
    list_filter = ('is_force', 'is_active', 'is_sent')
    raw_id_fields = ('user',)
    readonly_fields = ('target_user_count', 'read_user_count')
    search_fields = ("title",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'title', 'receiver', 'sender', 'task', 'is_force')
    list_filter = ('is_force', 'is_active', 'is_read')
    raw_id_fields = ('receiver', 'sender', 'task')
    search_fields = ("title",)
