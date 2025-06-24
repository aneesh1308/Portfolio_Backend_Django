from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Resume

User = get_user_model()

class Command(BaseCommand):
    help = 'Create admin user and display resumeId for frontend'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Admin email address')
        parser.add_argument('--password', type=str, help='Admin password')

    def handle(self, *args, **options):
        email = options['email'] or 'admin@portfolio.com'
        password = options['password'] or 'admin123'

        # Create or get admin user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'✅ Admin user created: {email}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Admin user already exists: {email}')
            )

        # Create or get resume
        resume, resume_created = Resume.objects.get_or_create(
            user=user,
            defaults={
                'email': email,
                'name': 'Admin Portfolio',
                'title': 'Full Stack Developer',
                'bio': 'Experienced developer with expertise in web technologies.',
                'phone_number': '+1234567890',
                'location': 'Remote',
            }
        )

        if resume_created:
            self.stdout.write(
                self.style.SUCCESS('✅ Resume created for admin user')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Resume already exists for admin user')
            )

        # Display important information
        self.stdout.write(
            self.style.SUCCESS('\n🎯 IMPORTANT INFORMATION FOR FRONTEND:')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📧 Admin Email: {user.email}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'🔑 Admin Password: {password}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'🆔 Admin User ID: {user.id}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📋 Resume ID: {resume.user_id}')
        )
        self.stdout.write(
            self.style.SUCCESS('\n💡 Use this Resume ID in your frontend:')
        )
        self.stdout.write(
            self.style.SUCCESS(f'const resumeId = "{resume.user_id}";')
        ) 