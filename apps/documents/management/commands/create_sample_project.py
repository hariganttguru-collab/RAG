from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.documents.models import Project, Document
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Create a sample project with document for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to create project for')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist.')
            )
            return

        # Create sample project
        project, created = Project.objects.get_or_create(
            name='E-Commerce Platform Redesign',
            user=user,
            defaults={
                'description': (
                    'A comprehensive redesign of the existing e-commerce platform '
                    'to improve user experience and increase conversion rates. '
                    'The project includes UI/UX redesign, backend optimization, '
                    'and mobile app development.'
                )
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created project: {project.name}')
            )
            
            # Create a sample project document (text file as placeholder)
            doc_path = os.path.join(settings.MEDIA_ROOT, 'documents')
            os.makedirs(doc_path, exist_ok=True)
            
            doc_file_path = os.path.join(doc_path, 'project_brief.txt')
            with open(doc_file_path, 'w') as f:
                f.write("""PROJECT BRIEF: E-Commerce Platform Redesign

PROJECT OVERVIEW:
This project involves a complete redesign of our existing e-commerce platform to enhance user experience and drive business growth.

KEY OBJECTIVES:
1. Improve user interface and user experience
2. Increase conversion rates by 25%
3. Enhance mobile responsiveness
4. Optimize backend performance
5. Implement new payment gateway integration

SCOPE:
- Frontend redesign (UI/UX)
- Backend API optimization
- Mobile app development
- Payment gateway integration
- Testing and QA

TIMELINE:
Target completion: 6 months

BUDGET:
Estimated budget: $500,000 - $750,000

STAKEHOLDERS:
- Senior Manager: Sarah Chen
- Team Lead: Mike Rodriguez
- Developer: Alex Kim
- Designer: Emma Watson
- QA Engineer: David Park
- Client: Robert Johnson

NEXT STEPS:
1. Review project requirements
2. Create detailed project estimation
3. Develop budget proposal
4. Get stakeholder approvals
""")
            
            document = Document.objects.create(
                project=project,
                title='Project Brief Document',
                file='documents/project_brief.txt',
                uploaded_by=user
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created document: {document.title}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Project already exists: {project.name}')
            )

        self.stdout.write(
            self.style.SUCCESS('Sample project setup complete!')
        )

