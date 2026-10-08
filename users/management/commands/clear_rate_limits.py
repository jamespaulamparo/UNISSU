from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clears all rate limit counters from the cache'

    def handle(self, *args, **options):
        # depending on cache backend, delete_pattern may or may not be available
        try:
            # attempt to delete all keys starting with rate_limit:
            cache.delete_pattern('rate_limit:*')
            self.stdout.write(self.style.SUCCESS('Rate limit keys cleared (pattern delete).'))
        except AttributeError:
            # fallback: if backend doesn't support delete_pattern, just clear entire cache
            cache.clear()
            self.stdout.write(self.style.WARNING(
                'Cache backend didn\'t support delete_pattern; entire cache flushed instead.'
            ))
        
        # The command does not raise errors so it can be run safely.
