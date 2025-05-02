from django.test import TestCase

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from desk.models import Project, Contributor, Issue, Comment

from authentication.models import CustomUser


class ProjectModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', age=16, password='password123')


    def test_create_project(self):
        project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            author=self.user,
            type='BACKEND'
        )
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.description, 'Test Description')
        self.assertEqual(project.author, self.user)
        self.assertEqual(project.type, 'BACKEND')


    def test_project_str(self):
        project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            author=self.user,
            type='BACKEND'
        )
        self.assertEqual(str(project), 'Test Project')


class ContributorModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', age=16, password='password123')
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            author=self.user,
            type='BACKEND'
        )

    def test_create_contributor(self):
        contributor = Contributor.objects.create(
            user=self.user,
            project=self.project,
            role='CONTRIBUTOR'
        )
        self.assertEqual(contributor.user, self.user)
        self.assertEqual(contributor.project, self.project)
        self.assertEqual(contributor.role, 'CONTRIBUTOR')

    def test_contributor_str(self):
        contributor = Contributor.objects.create(
            user=self.user,
            project=self.project,
            role='CONTRIBUTOR'
        )
        self.assertEqual(str(contributor), f"{self.user.username} -> {self.project.name} (CONTRIBUTOR)")

    def test_contributor_uniqueness(self):
        Contributor.objects.create(
            user=self.user,
            project=self.project,
            role='CONTRIBUTOR'
        )
        with self.assertRaises(IntegrityError):
            Contributor.objects.create(
                user=self.user,
                project=self.project,
                role='CONTRIBUTOR'
            )

class IssueModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', age=16, password='password123')
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            author=self.user,
            type='BACKEND'
        )

    def test_create_issue(self):
        issue = Issue.objects.create(
            title='Test Issue',
            description='Test Description',
            project=self.project,
            status='TODO',
            priority='MEDIUM',
            tag='BUG',
            author=self.user
        )
        self.assertEqual(issue.title, 'Test Issue')
        self.assertEqual(issue.description, 'Test Description')
        self.assertEqual(issue.project, self.project)
        self.assertEqual(issue.status, 'TODO')
        self.assertEqual(issue.priority, 'MEDIUM')
        self.assertEqual(issue.tag, 'BUG')
        self.assertEqual(issue.author, self.user)

    def test_issue_str(self):
        issue = Issue.objects.create(
            title='Test Issue',
            description='Test Description',
            project=self.project,
            status='TODO',
            priority='MEDIUM',
            tag='BUG',
            author=self.user
        )
        self.assertEqual(str(issue), 'Test Issue - Todo')


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', age=16, password='password123')
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            author=self.user,
            type='BACKEND'
        )
        self.issue = Issue.objects.create(
            title='Test Issue',
            description='Test Description',
            project=self.project,
            status='TODO',
            priority='MEDIUM',
            tag='BUG',
            author=self.user
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            issue=self.issue,
            author=self.user,
            content='Test Comment'
        )
        self.assertEqual(comment.issue, self.issue)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'Test Comment')

    def test_comment_str(self):
        comment = Comment.objects.create(
            issue=self.issue,
            author=self.user,
            content='Test Comment'
        )
        self.assertEqual(str(comment), f"Comment by {self.user.username} on {self.issue.title}")
