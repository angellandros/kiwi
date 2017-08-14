from datetime import datetime

from django.core.management.base import BaseCommand

from reports.models import Datum, Device


class Command(BaseCommand):
    help = 'Insert a csv file into DB'

    def add_arguments(self, parser):
        parser.add_argument('file', type=open)

    def handle(self, *args, **options):
        raw_data = []  # data read from the file
        devices = []  # list of device id's in the file
        data = []  # list of Datum objects to add to DB in one query

        # load the file into RAM
        for line in options['file']:
            if 'timestamp' in line:
                continue
            split_line = line.split(',')
            raw_data.append(split_line)
            device_id = split_line[1]
            if device_id not in devices:
                devices.append(device_id)
        del split_line
        del device_id
        # log, for keeping the track of data loss
        self.stdout.write(self.style.SUCCESS('Successfully loaded %d records' % len(raw_data)))

        # filter the new devices
        old_devices = [device.device_id for device in Device.objects.filter(device_id__in=devices)]
        new_devices = [d_id for d_id in devices if d_id not in old_devices]

        # add new devices into DB in one query
        Device.objects.bulk_create([Device(device_id=d_id) for d_id in new_devices])
        self.stdout.write(self.style.SUCCESS('Successfully added %d new device IDs' % len(new_devices)))

        # add the data
        created_num = 0  # number of device id's not yet in DB
        for raw_datum in raw_data:
            device_id = raw_datum[1]
            # this line won't create, but we have to make sure
            device, created = Device.objects.get_or_create(device_id=device_id)
            if created:
                created_num += 1
            try:
                data.append(Datum(
                    time=datetime.strptime(raw_datum[0], '%Y-%m-%dT%H:%M:%SZ'),
                    device=device,
                    type=1 if raw_datum[2] == 'sensor' else 2,
                    status=1 if 'offline' in raw_datum[3] else 2,
                ))
            except ValueError:
                self.stdout.write('Invalid timestamp format: %s' % split_line[0])
        # log, for keeping the track of data loss
        self.stdout.write(self.style.SUCCESS('Successfully parsed %d records' % len(data)))

        # this must not show, or we have not added all the device id's in the first time
        if created_num > 0:
            self.stdout.write('Added %d new devices during the parsing' % created_num)

        # add all the data with one query, and check if correct number of them are added
        object_num_then = Datum.objects.count()
        Datum.objects.bulk_create(data)
        object_num_diff = Datum.objects.count() - object_num_then
        # log, for keeping the track of data loss
        self.stdout.write(self.style.SUCCESS('Successfully created %d records in DB' % object_num_diff))
