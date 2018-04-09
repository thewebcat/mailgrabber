from django.core.management.base import BaseCommand, CommandError
from receiver.receiver import create_index, delete_index


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('action', type=str)

    def handle(self, *args, **options):
        if options['action'] == 'create':
            create_index()
        elif options['action'] == 'delete':
            delete_index()
        else:
            raise CommandError('Unknown option "{}". Available options is "create" or "delete"'.format(options['action']))
