from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from orders.models import Order
from products.models import Uniform
from users.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = 'Deletes unused user accounts (non-staff/superuser with no orders and no assigned products)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List users that would be deleted without actually removing them.',
        )

    def handle(self, *args, **options):
        # Eligible for deletion: non-superuser, non-staff, has profile with no assigned_products, no orders, active
        unused_users = User.objects.filter(
            is_superuser=False,
            is_staff=False,
            is_active=True,
            profile__assigned_products__isnull=True
        ).annotate(
            orders_count=Count('orders'),
            assigned_count=Count('profile__assigned_products')
        ).filter(
            orders_count=0,
            assigned_count=0
        ).distinct()

        count = unused_users.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No unused accounts found.'))
            return

        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f'{count} unused account(s) would be deleted:'))
            for u in unused_users:
                self.stdout.write(f'  - {u.username} ({u.email}) - Joined: {u.date_joined.date()}')
            return

        confirm = input(f'About to delete {count} unused user(s). Type YES to proceed: ')
        if confirm != 'YES':
            self.stdout.write(self.style.ERROR('Aborted.'))
            return

        deleted_count = unused_users.count()
        # Bulk delete cascades Profiles via on_delete=CASCADE
        unused_users.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} unused user(s).'))
