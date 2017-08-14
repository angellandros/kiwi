import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from reports.models import Device, Datum


class BulkCreateTest(TestCase):
    def test_bulk_create(self):
        out = StringIO()
        path = os.path.join(settings.BASE_DIR, 'ci/report.csv')
        call_command('bulk_create', path, stdout=out)

        self.assertIn('3 new device IDs', out.getvalue())
        self.assertEqual(Device.objects.count(), 3)
        self.assertEqual(Datum.objects.count(), 4)
        self.assertEqual(Datum.objects.filter(type=2).count(), 1)
        self.assertEqual(Datum.objects.filter(status=2).count(), 2)
