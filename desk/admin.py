from django.contrib import admin
from .models import Project, Contributor, Issue, Comment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'type', 'created_at', "id")
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'description')
    raw_id_fields = ('author',)

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'project__name')
    raw_id_fields = ('user', 'project')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'tag', 'assign', 'author', "id")
    list_filter = ('status', 'priority', 'tag', 'project')
    search_fields = ('title', 'description')
    raw_id_fields = ('project', 'assign', 'author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('issue', 'author', 'created_at', "id")
    list_filter = ('created_at',)
    search_fields = ('content',)
    raw_id_fields = ('issue', 'author')