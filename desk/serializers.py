from rest_framework import serializers

from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'author', 'type', 'created_at']
        read_only_fields = ['id', 'created_time']
        extra_kwargs = {
            'author': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'tag', 'assign', 'created_at']
        read_only_fields = ['id', 'author', 'project', 'created_at']
        extra_kwargs = {
            'author': {'required': False},
            'project': {'required': False}
        }

    def validate_assign(self, value):

        if value is None:
            return value

        project = self.context.get('project')
        if not project:
            raise serializers.ValidationError("Project context is missing.")

        # Check if the assigned user is project's contributor
        if value == project.author:
            return value
        if value and not Contributor.objects.filter(project=project, user=value).exists():
            raise serializers.ValidationError("This user is not a contributor of this project.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'issue', 'created_at']
        extra_kwargs = {
            'author': {'required': False},
            'issue': {'required': False}
        }
