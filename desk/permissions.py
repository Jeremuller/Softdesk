from rest_framework import permissions

from .models import Contributor

class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project=obj, user=request.user).exists()

class IsContributorIssue(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        project = obj.project
        return Contributor.objects.filter(project=project, user=request.user).exists()


class IsContributorComment(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        issue = obj.issue
        project = issue.project
        return Contributor.objects.filter(project=project, user=request.user).exists()