from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Deletes all user accounts except those marked as superuser'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List users that would be deleted without actually removing them.',
        )

    def handle(self, *args, **options):
        qs = User.objects.filter(is_superuser=False)
        # remove any leftover email verification entries (table may remain even though
        # the model was deleted) to avoid FK constraint errors
        try:
            from users.models import EmailVerification
            EmailVerification.objects.filter(user__in=qs).delete()
        except ImportError:
            # model removed; nothing to delete
            pass
        count = qs.count()
        if options['dry_run']:
            self.stdout.write(self.style.WARNING(
                f'{count} non-superuser account(s) would be deleted:'))
            for u in qs:
                self.stdout.write(f'  - {u.username} ({u.email})')
            return

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No non-superuser accounts to delete.'))
            return

        confirm = input(f'About to delete {count} user(s). Type YES to proceed: ')
        if confirm != 'YES':
            self.stdout.write(self.style.ERROR('Aborted.'))
            return

        qs.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} user(s).'))
