from django.core.management.base import BaseCommand
from apps.chat.models import Stakeholder


class Command(BaseCommand):
    help = 'Initialize default stakeholders'

    def handle(self, *args, **options):
        stakeholders_data = [
            {
                'name': 'Sarah Chen',
                'stakeholder_type': 'senior_manager',
                'avatar': '👩‍💼',
                'description': 'Senior Project Manager - Initiates projects and guides the team',
            },
            {
                'name': 'Mike Rodriguez',
                'stakeholder_type': 'team_lead',
                'avatar': '👨‍💻',
                'description': 'Technical Team Lead - Provides technical estimates and guidance',
            },
            {
                'name': 'Alex Kim',
                'stakeholder_type': 'developer',
                'avatar': '👨‍🔧',
                'description': 'Senior Developer - Estimates development work',
            },
            {
                'name': 'Emma Watson',
                'stakeholder_type': 'designer',
                'avatar': '👩‍🎨',
                'description': 'UX/UI Designer - Provides design estimates',
            },
            {
                'name': 'David Park',
                'stakeholder_type': 'qa',
                'avatar': '👨‍🔬',
                'description': 'QA Engineer - Estimates testing efforts',
            },
            {
                'name': 'Robert Johnson',
                'stakeholder_type': 'client',
                'avatar': '👔',
                'description': 'Client Representative - Represents business needs',
            },
        ]

        for data in stakeholders_data:
            stakeholder, created = Stakeholder.objects.get_or_create(
                name=data['name'],
                defaults={
                    'stakeholder_type': data['stakeholder_type'],
                    'avatar': data['avatar'],
                    'description': data['description'],
                    'is_online': True,
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created stakeholder: {stakeholder.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Stakeholder already exists: {stakeholder.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully initialized stakeholders!')
        )

