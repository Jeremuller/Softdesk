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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'issue', 'created_at']
        extra_kwargs = {
            'author': {'required': False},
            'issue': {'required': False}
        }
