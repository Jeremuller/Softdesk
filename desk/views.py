from rest_framework import viewsets, status
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def promote_contribution(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'detail':'User\'s ID required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.get(id=user_id)

        if project.author != request.user:
            return Response({'detail': 'You are not allowed to do this.'},
                            status=status.HTTP_403_FORBIDDEN)

        if Contributor.objects.filter(project=project, user=user).exists():
            return Response({'detail': 'This user is already contributing to this project.'},
                            status=status.HTTP_400_BAD_REQUEST)

        Contributor.objects.create(project=project, user=user, role='CONTRIBUTOR')
        return Response({'detail': 'user has been promoted to contributor.'},
                            status=status.HTTP_200_OK)

    def get_permissions(self):

        if self.action == 'create':
            self.permission_classes = IsAuthenticated

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAuthor]

        elif self.action in ['retrieve', 'list']:
            self.permission_classes = [IsAuthenticated, IsContributor | IsAuthor]

        return super().get_permissions()



class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsContributorIssue]

    def get_permissions(self):

        if self.action == 'create':
            self.permission_classes = [IsContributorIssue]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAuthor]

        elif self.action in ['retrieve', 'list']:
            self.permission_classes = [IsContributorIssue | IsAuthor]

        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsContributorComment]


    def get_permissions(self):

        if self.action == 'create':
            self.permission_classes = [IsContributorComment]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAuthor]

        elif self.action in ['retrieve', 'list']:
            self.permission_classes = [IsContributorComment | IsAuthor]

        return super().get_permissions()
