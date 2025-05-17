from rest_framework import permissions

from .models import Contributor

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(
            project=obj,
            user=request.user
        ).exists()

class IsContributorIssue(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(
            project=obj.project,
            user=request.user
        ).exists()

class IsContributorComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(
            project=obj.issue.project,
            user=request.user
        ).exists()