from rest_framework import serializers

from .models import Project, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

    def validate_assign(self, value):
        # Check if the assigned user is project's contributor
        if value and not Contributor.objects.filter(project=self.context['project'], user=value).exists():
            raise serializers.ValidationError("This user is not a contributor of this project.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields ='__all__'
