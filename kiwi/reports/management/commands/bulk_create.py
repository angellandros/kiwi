from datetime import datetime

from django.core.management.base import BaseCommand

from reports.models import Datum


class Command(BaseCommand):
    help = 'Insert a csv file into DB'

    def add_arguments(self, parser):
        parser.add_argument('file', type=open)

    def handle(self, *args, **options):
        data = []
        for line in options['file']:
            if 'timestamp' in line:
                continue
            split_line = line.split(',')
            try:
                data.append(Datum(
                    time=datetime.strptime(split_line[0], '%Y-%m-%dT%H:%M:%SZ'),
                    device_id=split_line[1],
                    type=1 if split_line[2] == 'sensor' else 2,
                    status=1 if split_line[3] == 'offline' else 2,
                ))
            except ValueError:
                self.stdout.write('Invalid timestamp format: %s' % split_line[0])
        self.stdout.write(self.style.SUCCESS('Successfully parsed %d records' % len(data)))
        object_num_then = Datum.objects.count()
        Datum.objects.bulk_create(data)
        object_num_diff = Datum.objects.count() - object_num_then
        self.stdout.write(self.style.SUCCESS('Successfully created %d records in DB' % object_num_diff))
