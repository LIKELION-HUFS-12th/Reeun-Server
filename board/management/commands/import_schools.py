import csv
from django.core.management.base import BaseCommand
from board.models import School, Board

class Command(BaseCommand):
    help = 'Import schools from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure the columns in your CSV file match the keys here
                School.objects.create(
                    city=row['시도명'],
                    school_type=row['학교종류명'],
                    school_name=row['학교명']
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported schools'))
