from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, Issue, Comment, Contributor
from authentication.models import CustomUser

from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer

from .permissions import IsAuthor, IsContributor, IsContributorIssue, IsContributorComment


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAuthor])
    def promote_contribution(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'detail':'User\'s ID required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.get(id=user_id)

        if Contributor.objects.filter(project=project, user=user).exists():
            return Response({'detail': 'This user is already contributing to this project.'},
                            status=status.HTTP_400_BAD_REQUEST)

        Contributor.objects.create(project=project, user=user, role='CONTRIBUTOR')
        return Response({'detail': 'user has been promoted to contributor.'},
                            status=status.HTTP_200_OK)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsContributor]

        return [permission() for permission in permission_classes]



class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_serializers_context(self):
        context = super().get_serializers_context()
        context['project'] = self.kwargs.get('project_pk')
        return context

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsContributorIssue]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]

        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, (IsContributorIssue | IsAuthor)]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsContributor])
    def update_status(self, request, pk=None):
        issue = self.get_object
        new_status = request.data.get('status')

        if not new_status:
            return Response({'detail': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_status not in [choice[0] for choice in Issue.STATUS]:
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        issue.status = new_status
        issue.save()
        return Response({'detail': 'Status updated successfully.'}, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsContributorComment]


    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsContributorComment]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]

        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, (IsContributorComment | IsAuthor)]

        return [permission() for permission in permission_classes]
